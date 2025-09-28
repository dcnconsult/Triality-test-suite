"""
analysis/plot_focused.py
Plot CI whiskers for selected PLV/PAC metrics across g12 values (sliced by g13,g23,lam).
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

def whisker_plot(df, metric, group_cols, x_col="g12", outpath="plot.png"):
    """
    Group by group_cols, then for each group plot metric CI over x_col.
    """
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    groups = df.groupby(group_cols)
    for key, sub in groups:
        sub = sub.sort_values(x_col)
        plt.figure()
        x = sub[x_col].values
        y = sub[f"{metric}_boot_mean"].values
        lo = sub[f"{metric}_ci_lo"].values
        hi = sub[f"{metric}_ci_hi"].values
        plt.errorbar(x, y, yerr=[y-lo, hi-y], fmt='o-')
        plt.xlabel(x_col)
        ttl = f"{metric} vs {x_col} | " + ", ".join([f"{c}={v}" for c,v in zip(group_cols, key if isinstance(key, tuple) else (key,))])
        plt.title(ttl)
        plt.tight_layout()
        plt.savefig(outpath.replace(".png", f"_{'_'.join(map(str,key if isinstance(key, tuple) else (key,)))}.png"), dpi=160)
        plt.close()

def main(csv_path="/mnt/data/triality_focused_results.csv", out_dir="/mnt/data/plots_focused"):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    # Choose to slice by (g13, g23, lam) and plot against g12
    group_cols = ["g13", "g23", "lam"]
    for metric in ["plv_low_12", "plv_mid_23", "plv_high_13", "pac_low_high_13", "pac_low_mid_12"]:
        outpath = os.path.join(out_dir, f"{metric}_whiskers.png")
        whisker_plot(df, metric, group_cols, x_col="g12", outpath=outpath)

if __name__ == "__main__":
    main()
