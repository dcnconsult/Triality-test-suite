"""
analysis/detuning_aggregate.py
Aggregate detuning vs. triad metrics across platforms (JPC & SPDC).

Sources:
- /mnt/data/jpc_batch_summary.csv
- /mnt/data/spdc_batch_summary.csv
Optional metadata (JSON): maps filename (stem) -> detuning value (Hz or GHz as you choose).
- /mnt/data/jpc_detuning_meta.json
- /mnt/data/spdc_detuning_meta.json

If 'detuning' column not present in a summary, this script attempts to:
  1) load the corresponding meta JSON;
  2) else parse from filename using regex patterns:
       r'det([-+]?[0-9]*\.?[0-9]+)' or r'run[_-]?(\d+)' (ordinal as proxy).

Outputs:
- /mnt/data/detuning_aggregated.csv (platform, file, detuning, b2_peak, peak_z, coh_time)
- Plots in /mnt/data/universality_plots/
"""
import os, re, json, pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

def _inject_detuning(df, meta_json, platform):
    df = df.copy()
    if "detuning" in df.columns:
        return df
    # Try metadata
    meta = {}
    if os.path.exists(meta_json):
        with open(meta_json, "r") as f:
            meta = json.load(f)
    dets = []
    for fpath in df["file"]:
        stem = Path(fpath).stem
        val = None
        if stem in meta:
            val = meta[stem]
        else:
            m = re.search(r"det([-+]?[0-9]*\.?[0-9]+)", stem, re.IGNORECASE)
            if m:
                val = float(m.group(1))
            else:
                m2 = re.search(r"run[_-]?(\d+)", stem, re.IGNORECASE)
                if m2:
                    val = float(m2.group(1))
        dets.append(val if val is not None else np.nan)
    df["detuning"] = dets
    return df

def plot_detuning(df, platform, outdir):
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(df["detuning"], df["b2_peak"], marker='o')
    plt.ylabel("b2_peak")
    plt.title(f"{platform}: Triad metrics vs detuning")
    plt.subplot(3,1,2)
    plt.plot(df["detuning"], df["peak_z"], marker='o')
    plt.ylabel("z-score")
    plt.subplot(3,1,3)
    col = "coh_time_ge_0.5" if "coh_time_ge_0.5" in df.columns else "coh_time"
    if col not in df.columns:
        df[col] = np.nan
    plt.plot(df["detuning"], df[col], marker='o')
    plt.xlabel("detuning (arb. units)"); plt.ylabel("coh_time ≥0.5 (s)")
    plt.tight_layout()
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, f"{platform.lower()}_metrics_vs_detuning.png")
    plt.savefig(p, dpi=160); plt.close()
    return p

def main(jpc_csv="/mnt/data/jpc_batch_summary.csv",
         spdc_csv="/mnt/data/spdc_batch_summary.csv",
         out_csv="/mnt/data/detuning_aggregated.csv",
         out_dir="/mnt/data/universality_plots"):
    rows = []
    paths = []
    if os.path.exists(jpc_csv):
        jdf = pd.read_csv(jpc_csv)
        jdf = _inject_detuning(jdf, "/mnt/data/jpc_detuning_meta.json", "JPC")
        jdf["platform"] = "JPC"
        paths.append(plot_detuning(jdf.sort_values("detuning"), "JPC", out_dir))
        rows.append(jdf)
    if os.path.exists(spdc_csv):
        sdf = pd.read_csv(spdc_csv)
        sdf = _inject_detuning(sdf, "/mnt/data/spdc_detuning_meta.json", "SPDC")
        sdf["platform"] = "SPDC"
        paths.append(plot_detuning(sdf.sort_values("detuning"), "SPDC", out_dir))
        rows.append(sdf)
    if rows:
        all_df = pd.concat(rows, ignore_index=True)
        all_df[["platform","file","detuning","b2_peak","peak_z","coh_time_ge_0.5" if "coh_time_ge_0.5" in all_df.columns else "coh_time"]].to_csv(out_csv, index=False)
    print("Wrote:", out_csv if rows else "No outputs (no summaries found).")
    for p in paths:
        print("Plot:", p)

if __name__ == "__main__":
    main()
