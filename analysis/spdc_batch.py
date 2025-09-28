"""
analysis/spdc_batch.py
Batch analysis for SPDC time-tag JSON/CSV/NPZ files:
- Bin event times to counts
- Compute cross-bicoherence and surrogate z-scores
- Compute triad lock-phase stability on binned counts
- Save summary CSV and annotated hotspot plots
"""
import os, glob, json, numpy as np, pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
from analysis.event_binning import load_event_times, bin_events
from analysis.bispectrum import cross_bispectrum
from analysis.bispec_peaks import find_bicoherence_peak, dominant_freq
from analysis.surrogates import phase_randomize, peak_zscore
from analysis.triad_lock import triad_phase_lock, triad_phase_lock_sliding, coherence_time
from analysis.plot_bispec_with_peak import plot as plot_annot

def analyze_file(path, outdir="/mnt/data/spdc_plots", fs_bin=1e6, seglen=131072, B=50, bw=1.0, win_s=0.5, step_s=0.1, seed=7):
    os.makedirs(outdir, exist_ok=True)
    ch_times = load_event_times(path)
    t, X = bin_events(ch_times, fs=fs_bin, T=None, t0=None)  # X: (N, 3)
    fs = fs_bin

    # Cross-bicoherence on binned counts
    f, Sxyz, b2 = cross_bispectrum(X[:,0], X[:,1], X[:,2], fs, seglen=seglen, step=None)
    peak = find_bicoherence_peak(b2, f)

    # Surrogates (phase-shuffle binned counts)
    rng = np.random.default_rng(seed)
    null_peaks = []
    for b in range(B):
        xs = phase_randomize(X[:,0], seed=rng.integers(0,1e9))
        ys = phase_randomize(X[:,1], seed=rng.integers(0,1e9))
        zs = phase_randomize(X[:,2], seed=rng.integers(0,1e9))
        _, _, b2s = cross_bispectrum(xs, ys, zs, fs, seglen=seglen, step=None)
        null_peaks.append(b2s.max())
    zscore, pval, mu, sd = peak_zscore(peak["b2_peak"], null_peaks)

    # Lock-phase stability on binned counts (treat counts as intensity time series)
    # Estimate band centers from individual spectra
    f1_est = float(dominant_freq(X[:,0], fs, nmax=1)[0][0])
    f2_est = float(dominant_freq(X[:,1], fs, nmax=1)[0][0])
    L_static = triad_phase_lock(X[:,0], X[:,1], X[:,2], fs, f1_est, f2_est, bw=bw)
    idxs, L_vals = triad_phase_lock_sliding(X[:,0], X[:,1], X[:,2], fs, f1_est, f2_est, bw=bw, win_s=win_s, step_s=step_s)
    coh_t = coherence_time(idxs, L_vals, thresh=0.5)

    # Plots
    outpng = os.path.join(outdir, Path(path).stem + "_bicoherence_cross_annot.png")
    plot_annot(f, b2, peak, f3_est=None, outpng=outpng)
    # Lock plot
    plt.figure()
    plt.plot(idxs, L_vals)
    plt.axhline(0.5, linestyle="--")
    plt.xlabel("time (s)"); plt.ylabel("triad lock L(t)")
    plt.title(f"{os.path.basename(path)} | L_static={L_static:.3f} | CohT≥0.5={coh_t:.2f}s")
    png_lock = os.path.join(outdir, Path(path).stem + "_lock.png")
    plt.tight_layout(); plt.savefig(png_lock, dpi=160); plt.close()

    row = {
        "file": path, "fs_bin": fs_bin, "seglen": seglen,
        "f1_peak": peak["f1"], "f2_peak": peak["f2"], "b2_peak": peak["b2_peak"],
        "peak_z": zscore, "peak_p": pval, "null_mean": mu, "null_sd": sd,
        "f1_est": f1_est, "f2_est": f2_est, "L_static": L_static, "coh_time_ge_0.5": coh_t
    }
    return row, outpng, png_lock

def main(glob_pattern="/mnt/data/spdc_detuned_run_*.json", out_csv="/mnt/data/spdc_batch_summary.csv",
         outdir="/mnt/data/spdc_plots", fs_bin=1e6, seglen=131072, B=50):
    files = sorted(glob.glob(glob_pattern))
    rows = []
    for fpath in files:
        try:
            row, p1, p2 = analyze_file(fpath, outdir=outdir, fs_bin=fs_bin, seglen=seglen, B=B)
            rows.append(row)
            print("Analyzed:", fpath, "peak b2:", row["b2_peak"], "z≈", row["peak_z"], "cohT≈", row["coh_time_ge_0.5"])
        except Exception as e:
            print("Error:", fpath, ":", e)
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(out_csv, index=False)
        print("Wrote summary:", out_csv, "rows:", len(df))
    else:
        print("No files matched", glob_pattern)

if __name__ == "__main__":
    main()
