"""
analysis/plot_adaptive.py
Plot top-k adaptive results and compare to seed ranking.
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUT_DIR = PROJECT_ROOT / "out"

DEFAULT_RESULTS = OUT_DIR / "triality_adaptive_results.csv"
DEFAULT_PLOTS = OUT_DIR / "plots_adaptive"


def plot_topk(csv_path=DEFAULT_RESULTS, out_dir=DEFAULT_PLOTS, top_k=20):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(csv_path)
    df = df.sort_values("objective", ascending=False).head(top_k).copy()

    for param in ["g12", "g13", "g23", "lam"]:
        plt.figure()
        plt.scatter(df[param], df["objective"])
        plt.xlabel(param)
        plt.ylabel("objective")
        plt.title(f"Objective vs {param} (top {top_k})")
        plt.tight_layout()
        plt.savefig(out_dir / f"objective_vs_{param}.png", dpi=160)
        plt.close()

    plt.figure()
    cols = [
        "plv_low_12",
        "plv_mid_23",
        "plv_high_13",
        "pac_low_high_13",
        "pac_low_mid_12",
        "objective",
    ]
    corr = df[cols].corr()
    im = plt.imshow(corr, interpolation="nearest")
    plt.xticks(range(corr.shape[1]), corr.columns, rotation=45, ha="right")
    plt.yticks(range(corr.shape[0]), corr.index)
    plt.title("Metric Correlations (top subset)")
    plt.colorbar(im)
    plt.tight_layout()
    plt.savefig(out_dir / "metric_correlations.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    plot_topk()
