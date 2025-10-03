"""
analysis/jpc_lock_batch.py
For each JPC CSV, estimate dominant mode frequencies, compute static and sliding
triad phase-lock index, and save plots plus a summary table.
"""
import glob
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.load_timeseries import load_timeseries
from analysis.bispec_peaks import dominant_freq
from analysis.triad_lock import triad_phase_lock, triad_phase_lock_sliding, coherence_time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUT_DIR = PROJECT_ROOT / "out"

DEFAULT_OUTDIR = OUT_DIR / "jpc_lock_plots"
DEFAULT_GLOB_PATTERN = DATA_DIR / "jpc_run_*.csv"
DEFAULT_SUMMARY = OUT_DIR / "jpc_lock_summary.csv"


def analyze_file(path, outdir=DEFAULT_OUTDIR, bw=1.0, win_s=1.0, step_s=0.25):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    t, X, cols = load_timeseries(path)
    dt = np.median(np.diff(t))
    fs = 1.0 / dt

    def pick(name):
        return X[:, cols.index(name)] if name in cols else None

    x = pick("mode1_I")
    y = pick("mode2_I")
    z = pick("mode3_I")
    if x is None or y is None or z is None:
        raise ValueError("Expected columns: mode1_I, mode2_I, mode3_I")

    f1_est = float(dominant_freq(x, fs, nmax=1)[0][0])
    f2_est = float(dominant_freq(y, fs, nmax=1)[0][0])
    L_static = triad_phase_lock(x, y, z, fs, f1_est, f2_est, bw=bw)
    idxs, L_vals = triad_phase_lock_sliding(
        x,
        y,
        z,
        fs,
        f1_est,
        f2_est,
        bw=bw,
        win_s=win_s,
        step_s=step_s,
    )
    coh_t = coherence_time(idxs, L_vals, thresh=0.5)

    plt.figure()
    plt.plot(idxs, L_vals)
    plt.axhline(0.5, linestyle="--")
    plt.xlabel("time (s)")
    plt.ylabel("triad lock L(t)")
    plt.title(f"{Path(path).name} | L_static={L_static:.3f} | CohT>=0.5={coh_t:.2f}s")
    png = outdir / f"{Path(path).stem}_lock.png"
    plt.tight_layout()
    plt.savefig(png, dpi=160)
    plt.close()

    return {
        "file": str(path),
        "fs": fs,
        "f1_est": f1_est,
        "f2_est": f2_est,
        "L_static": L_static,
        "coh_time_ge_0.5": coh_t,
    }, str(png)


def main(glob_pattern=DEFAULT_GLOB_PATTERN, out_csv=DEFAULT_SUMMARY,
         bw=1.0, win_s=1.0, step_s=0.25):
    pattern = str(glob_pattern)
    files = sorted(glob.glob(pattern))
    rows = []
    for fpath in files:
        try:
            row, png = analyze_file(fpath, bw=bw, win_s=win_s, step_s=step_s)
            rows.append(row)
            print("Lock:", fpath, "L_static~", row["L_static"], "CohT>=0.5~", row["coh_time_ge_0.5"])
        except Exception as exc:
            print("Error:", fpath, exc)
    if rows:
        out_csv = Path(out_csv)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(rows)
        df.to_csv(out_csv, index=False)
        print("Wrote", out_csv)
    else:
        print("No files matched", pattern)


if __name__ == "__main__":
    main()
