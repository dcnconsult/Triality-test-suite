"""
analysis/detuning_aggregate.py
Aggregate detuning vs. triad metrics across platforms (JPC & SPDC).

Sources (relative to the repository root):
- out/jpc_batch_summary.csv
- out/spdc_batch_summary.csv
Optional metadata (JSON) maps filename (stem) -> detuning value (Hz or GHz as you choose).
- data/jpc_detuning_meta.json
- data/spdc_detuning_meta.json

Outputs:
- out/detuning_aggregated.csv (platform, file, detuning, b2_peak, peak_z, coherence time)
- Plots in out/universality_plots/
"""
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUT_DIR = PROJECT_ROOT / "out"

DEFAULT_JPC_SUMMARY = OUT_DIR / "jpc_batch_summary.csv"
DEFAULT_SPDC_SUMMARY = OUT_DIR / "spdc_batch_summary.csv"
DEFAULT_OUT_CSV = OUT_DIR / "detuning_aggregated.csv"
DEFAULT_OUT_DIR = OUT_DIR / "universality_plots"
DEFAULT_JPC_META = DATA_DIR / "jpc_detuning_meta.json"
DEFAULT_SPDC_META = DATA_DIR / "spdc_detuning_meta.json"


def _inject_detuning(df, meta_json, platform):
    df = df.copy()
    if "detuning" in df.columns:
        return df

    meta_path = Path(meta_json)
    meta = {}
    if meta_path.exists():
        with open(meta_path, "r") as f:
            meta = json.load(f)

    dets = []
    for fpath in df["file"]:
        stem = Path(fpath).stem
        val = meta.get(stem)
        if val is None:
            match = re.search(r"det([-+]?[0-9]*\.?[0-9]+)", stem, re.IGNORECASE)
            if match:
                val = float(match.group(1))
            else:
                match = re.search(r"run[_-]?(\d+)", stem, re.IGNORECASE)
                if match:
                    val = float(match.group(1))
        dets.append(val if val is not None else np.nan)
    df["detuning"] = dets
    return df


def plot_detuning(df, platform, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(df["detuning"], df["b2_peak"], marker="o")
    plt.ylabel("b2_peak")
    plt.title(f"{platform}: Triad metrics vs detuning")

    plt.subplot(3, 1, 2)
    plt.plot(df["detuning"], df["peak_z"], marker="o")
    plt.ylabel("z-score")

    plt.subplot(3, 1, 3)
    col = "coh_time_ge_0.5" if "coh_time_ge_0.5" in df.columns else "coh_time"
    if col not in df.columns:
        df[col] = np.nan
    plt.plot(df["detuning"], df[col], marker="o")
    plt.xlabel("detuning (arb. units)")
    plt.ylabel("coh_time>=0.5 (s)")

    plt.tight_layout()
    out_path = outdir / f"{platform.lower()}_metrics_vs_detuning.png"
    plt.savefig(out_path, dpi=160)
    plt.close()
    return out_path


def main(jpc_csv=DEFAULT_JPC_SUMMARY, spdc_csv=DEFAULT_SPDC_SUMMARY,
         out_csv=DEFAULT_OUT_CSV, out_dir=DEFAULT_OUT_DIR,
         jpc_meta=DEFAULT_JPC_META, spdc_meta=DEFAULT_SPDC_META):
    rows = []
    plots = []

    jpc_csv = Path(jpc_csv)
    spdc_csv = Path(spdc_csv)
    out_csv = Path(out_csv)
    out_dir = Path(out_dir)

    if jpc_csv.exists():
        jdf = pd.read_csv(jpc_csv)
        jdf = _inject_detuning(jdf, jpc_meta, "JPC")
        jdf["platform"] = "JPC"
        plots.append(plot_detuning(jdf.sort_values("detuning"), "JPC", out_dir))
        rows.append(jdf)

    if spdc_csv.exists():
        sdf = pd.read_csv(spdc_csv)
        sdf = _inject_detuning(sdf, spdc_meta, "SPDC")
        sdf["platform"] = "SPDC"
        plots.append(plot_detuning(sdf.sort_values("detuning"), "SPDC", out_dir))
        rows.append(sdf)

    if rows:
        all_df = pd.concat(rows, ignore_index=True)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        select_col = "coh_time_ge_0.5" if "coh_time_ge_0.5" in all_df.columns else "coh_time"
        cols = ["platform", "file", "detuning", "b2_peak", "peak_z", select_col]
        all_df[cols].to_csv(out_csv, index=False)
        print("Wrote:", out_csv)
    else:
        print("No summaries found; nothing written.")

    for p in plots:
        print("Plot:", p)


if __name__ == "__main__":
    main()
