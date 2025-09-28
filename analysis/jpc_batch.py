"""
analysis/jpc_batch.py
Batch analysis for JPC CSV files:
- Load time series
- Compute cross-bicoherence among (mode1, mode2, mode3)
- Extract peak and estimate significance via phase-shuffled surrogates
- Save summary CSV and annotated plots
"""
import os, glob, numpy as np, pandas as pd
from analysis.load_timeseries import load_timeseries
from analysis.bispectrum import cross_bispectrum
from analysis.bispec_peaks import dominant_freq, find_bicoherence_peak
from analysis.surrogates import phase_randomize, peak_zscore
from analysis.plot_bispec_with_peak import plot as plot_annot

def analyze_file(path, outdir="/mnt/data/jpc_batch_plots", seglen=4096, step=None, ch_names=("mode1_I","mode2_I","mode3_I"), B=50, seed=7):
    os.makedirs(outdir, exist_ok=True)
    t, X, cols = load_timeseries(path)
    dt = np.median(np.diff(t)); fs = 1.0/dt
    # channel selection
    idx = []
    for name in ch_names:
        if isinstance(name, int):
            idx.append(name)
        else:
            idx.append(cols.index(name))
    x, y, z = X[:, idx[0]], X[:, idx[1]], X[:, idx[2]]

    # Cross-bicoherence
    f, Sxyz, b2 = cross_bispectrum(x, y, z, fs, seglen=seglen, step=step)
    peak = find_bicoherence_peak(b2, f)

    # Estimate f3 from PSD of z
    fz, mz = dominant_freq(z, fs, nmax=1)
    f3_est = float(fz[0]) if len(fz)>0 else None

    # Surrogate significance
    null_peaks = []
    rng = np.random.default_rng(seed)
    for b in range(B):
        xs = phase_randomize(x, seed=rng.integers(0,1e9))
        ys = phase_randomize(y, seed=rng.integers(0,1e9))
        zs = phase_randomize(z, seed=rng.integers(0,1e9))
        _, _, b2s = cross_bispectrum(xs, ys, zs, fs, seglen=seglen, step=step)
        null_peaks.append(b2s.max())
    zscore, pval, mu, sd = peak_zscore(peak["b2_peak"], null_peaks)

    # Save plot
    outpng = os.path.join(outdir, Path(path).stem + "_bicoherence_cross_annot.png")
    plot_annot(f, b2, peak, f3_est=f3_est, outpng=outpng)

    # Summary row
    row = {
        "file": path, "fs": fs, "seglen": seglen,
        "f1_peak": peak["f1"], "f2_peak": peak["f2"], "b2_peak": peak["b2_peak"],
        "f3_est": f3_est, "peak_z": zscore, "peak_p": pval, "null_mean": mu, "null_sd": sd
    }
    return row, outpng

def main(glob_pattern="/mnt/data/jpc_run_*.csv", out_csv="/mnt/data/jpc_batch_summary.csv",
         outdir="/mnt/data/jpc_batch_plots", seglen=4096, step=None, B=50):
    files = sorted(glob.glob(glob_pattern))
    results = []
    for fpath in files:
        try:
            row, outpng = analyze_file(fpath, outdir=outdir, seglen=seglen, step=step, B=B)
            results.append(row)
            print("Analyzed:", fpath, "peak b2:", row["b2_peak"], "z≈", row["peak_z"])
        except Exception as e:
            print("Error on", fpath, ":", e)
    if results:
        df = pd.DataFrame(results)
        df.to_csv(out_csv, index=False)
        print("Wrote summary:", out_csv, "rows:", len(df))
    else:
        print("No files matched", glob_pattern)

if __name__ == "__main__":
    from pathlib import Path
    main()
