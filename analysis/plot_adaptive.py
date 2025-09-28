"""
analysis/plot_adaptive.py
Plot top-k adaptive results and compare to seed ranking.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_topk(csv_path="/mnt/data/triality_adaptive_results.csv", out_dir="/mnt/data/plots_adaptive", top_k=20):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    df = df.sort_values("objective", ascending=False).head(top_k).copy()

    # Scatter of objective vs parameters
    for param in ["g12","g13","g23","lam"]:
        plt.figure()
        plt.scatter(df[param], df["objective"])
        plt.xlabel(param); plt.ylabel("objective")
        plt.title(f"Objective vs {param} (top {top_k})")
        plt.tight_layout()
        plt.savefig(f"{out_dir}/objective_vs_{param}.png", dpi=160)
        plt.close()

    # Correlation heatmap (simple)
    plt.figure()
    corr = df[["plv_low_12","plv_mid_23","plv_high_13","pac_low_high_13","pac_low_mid_12","objective"]].corr()
    im = plt.imshow(corr, interpolation='nearest')
    plt.xticks(range(corr.shape[1]), corr.columns, rotation=45, ha='right')
    plt.yticks(range(corr.shape[0]), corr.index)
    plt.title("Metric Correlations (top subset)")
    plt.colorbar(im)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/metric_correlations.png", dpi=160)
    plt.close()

if __name__ == "__main__":
    plot_topk()
