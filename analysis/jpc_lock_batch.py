"""
analysis/jpc_lock_batch.py
For each JPC CSV, estimate dominant mode frequencies, compute static and sliding
triad phase-lock index, and save plots + summary.
"""
import os, glob, numpy as np, pandas as pd, matplotlib.pyplot as plt
from analysis.load_timeseries import load_timeseries
from analysis.bispec_peaks import dominant_freq
from analysis.triad_lock import triad_phase_lock, triad_phase_lock_sliding, coherence_time

def analyze_file(path, outdir="/mnt/data/jpc_lock_plots", bw=1.0, win_s=1.0, step_s=0.25):
    os.makedirs(outdir, exist_ok=True)
    t, X, cols = load_timeseries(path)
    dt = np.median(np.diff(t)); fs = 1.0/dt
    # map channels by name heuristics
    def pick(name): return X[:, cols.index(name)] if name in cols else None
    x = pick("mode1_I"); y = pick("mode2_I"); z = pick("mode3_I")
    if x is None or y is None or z is None:
        raise ValueError("Expected columns: mode1_I, mode2_I, mode3_I")

    # estimate mode centers from spectra (rough but adequate for bandpass)
    f1_est = float(dominant_freq(x, fs, nmax=1)[0][0])
    f2_est = float(dominant_freq(y, fs, nmax=1)[0][0])
    # static lock
    L_static = triad_phase_lock(x, y, z, fs, f1_est, f2_est, bw=bw)
    # sliding
    idxs, L_vals = triad_phase_lock_sliding(x, y, z, fs, f1_est, f2_est, bw=bw, win_s=win_s, step_s=step_s)
    coh_t = coherence_time(idxs, L_vals, thresh=0.5)

    # plot
    plt.figure()
    plt.plot(idxs, L_vals)
    plt.axhline(0.5, linestyle="--")
    plt.xlabel("time (s)"); plt.ylabel("triad lock L(t)")
    plt.title(f"{os.path.basename(path)} | L_static={L_static:.3f} | CohT≥0.5={coh_t:.2f}s")
    png = os.path.join(outdir, os.path.splitext(os.path.basename(path))[0] + "_lock.png")
    plt.tight_layout(); plt.savefig(png, dpi=160); plt.close()

    return {"file": path, "fs": fs, "f1_est": f1_est, "f2_est": f2_est, "L_static": L_static, "coh_time_ge_0.5": coh_t}, png

def main(glob_pattern="/mnt/data/jpc_run_*.csv", out_csv="/mnt/data/jpc_lock_summary.csv", bw=1.0, win_s=1.0, step_s=0.25):
    files = sorted(glob.glob(glob_pattern))
    rows = []
    for f in files:
        try:
            row, png = analyze_file(f, bw=bw, win_s=win_s, step_s=step_s)
            rows.append(row)
            print("Lock:", f, "L_static≈", row["L_static"], "CohT≥0.5≈", row["coh_time_ge_0.5"])
        except Exception as e:
            print("Error:", f, e)
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(out_csv, index=False)
        print("Wrote", out_csv)
    else:
        print("No files matched", glob_pattern)

if __name__ == "__main__":
    main()
