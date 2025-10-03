"""
analysis/jpc_batch.py
Batch analysis for JPC CSV files:
- Load time series
- Compute cross-bicoherence among (mode1, mode2, mode3)
- Extract peak and estimate significance via phase-shuffled surrogates
- Save summary CSV and annotated plots
"""
import glob
import os
from pathlib import Path

import numpy as np
import pandas as pd

from analysis.load_timeseries import load_timeseries
from analysis.bispectrum import cross_bispectrum
from analysis.bispec_peaks import dominant_freq, find_bicoherence_peak
from analysis.surrogates import phase_randomize, peak_zscore
from analysis.plot_bispec_with_peak import plot as plot_annot

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUT_DIR = PROJECT_ROOT / "out"

DEFAULT_OUTDIR = OUT_DIR / "jpc_batch_plots"
DEFAULT_GLOB_PATTERN = DATA_DIR / "synthetic" / "triad_*.csv"
DEFAULT_SUMMARY = OUT_DIR / "jpc_batch_summary.csv"


def analyze_file(path, outdir=DEFAULT_OUTDIR, seglen=4096, step=None,
                 ch_names=("mode1_I", "mode2_I", "mode3_I"), B=50, seed=7):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    t, X, cols = load_timeseries(path)
    dt = np.median(np.diff(t))
    fs = 1.0 / dt

    idx = []
    for name in ch_names:
        if isinstance(name, int):
            idx.append(name)
        else:
            idx.append(cols.index(name))
    x, y, z = X[:, idx[0]], X[:, idx[1]], X[:, idx[2]]

    f, Sxyz, b2 = cross_bispectrum(x, y, z, fs, seglen=seglen, step=step)
    peak = find_bicoherence_peak(b2, f)

    fz, _ = dominant_freq(z, fs, nmax=1)
    f3_est = float(fz[0]) if len(fz) > 0 else None

    null_peaks = []
    rng = np.random.default_rng(seed)
    for _ in range(B):
        xs = phase_randomize(x, seed=rng.integers(0, 1_000_000_000))
        ys = phase_randomize(y, seed=rng.integers(0, 1_000_000_000))
        zs = phase_randomize(z, seed=rng.integers(0, 1_000_000_000))
        _, _, b2s = cross_bispectrum(xs, ys, zs, fs, seglen=seglen, step=step)
        null_peaks.append(b2s.max())
    zscore, pval, mu, sd = peak_zscore(peak["b2_peak"], null_peaks)

    outpng = outdir / f"{Path(path).stem}_bicoherence_cross_annot.png"
    plot_annot(f, b2, peak, f3_est=f3_est, outpng=str(outpng))

    row = {
        "file": str(path),
        "fs": fs,
        "seglen": seglen,
        "f1_peak": peak["f1"],
        "f2_peak": peak["f2"],
        "b2_peak": peak["b2_peak"],
        "f3_est": f3_est,
        "peak_z": zscore,
        "peak_p": pval,
        "null_mean": mu,
        "null_sd": sd,
    }
    return row, str(outpng)


def main(glob_pattern=DEFAULT_GLOB_PATTERN, out_csv=DEFAULT_SUMMARY,
         outdir=DEFAULT_OUTDIR, seglen=4096, step=None, B=50):
    pattern = str(glob_pattern)
    files = sorted(glob.glob(pattern))
    results = []
    for fpath in files:
        try:
            row, outpng = analyze_file(fpath, outdir=outdir, seglen=seglen, step=step, B=B)
            results.append(row)
            print("Analyzed:", fpath, "peak b2:", row["b2_peak"], "z~", row["peak_z"])
        except Exception as exc:
            print("Error on", fpath, ":", exc)
    if results:
        out_csv = Path(out_csv)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(results)
        df.to_csv(out_csv, index=False)
        print("Wrote summary:", out_csv, "rows:", len(df))
    else:
        print("No files matched", pattern)


if __name__ == "__main__":
    main()
