"""
analysis/plot_sweep.py
Load sweep CSV and generate simple plots for PLV and PAC metrics.
Each chart is a separate figure (no subplots).
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

def scatter_metric(df, x, y, metric, outpath):
    plt.figure()
    sc = plt.scatter(df[x], df[y], c=df[metric])
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"{metric} vs {x},{y}")
    cbar = plt.colorbar(sc)
    cbar.set_label(metric)
    plt.tight_layout()
    plt.savefig(outpath, dpi=160)
    plt.close()

def main(csv_path="triality_sweep_results.csv", out_dir="plots"):
    df = pd.read_csv(csv_path)
    os.makedirs(out_dir, exist_ok=True)

    # Choose a 2D slice by fixing g13 to its middle value if present
    if "g13" in df.columns:
        mid = sorted(df["g13"].unique())[1] if len(df["g13"].unique())>=3 else df["g13"].median()
        sdf = df[df["g13"]==mid].copy()
    else:
        sdf = df.copy()

    metrics = [c for c in df.columns if c.startswith("plv_") or c.startswith("pac_")]
    # Default axes
    x, y = "g12", "g23"
    for m in metrics:
        out = f"{out_dir}/{m}_vs_{x}_{y}.png"
        scatter_metric(sdf, x, y, m, out)

if __name__ == "__main__":
    import os
    main()
