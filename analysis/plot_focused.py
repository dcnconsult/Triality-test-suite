"""
analysis/plot_focused.py
Plot CI whiskers for selected PLV/PAC metrics across g12 values (sliced by g13, g23, lam).
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "out"

DEFAULT_RESULTS = OUT_DIR / "triality_focused_results.csv"
DEFAULT_PLOTS = OUT_DIR / "plots_focused"


def whisker_plot(df, metric, group_cols, x_col="g12", outpath=Path("plot.png")):
    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    groups = df.groupby(group_cols)
    for key, sub in groups:
        sub = sub.sort_values(x_col)
        plt.figure()
        x = sub[x_col].values
        y = sub[f"{metric}_boot_mean"].values
        lo = sub[f"{metric}_ci_lo"].values
        hi = sub[f"{metric}_ci_hi"].values
        plt.errorbar(x, y, yerr=[y - lo, hi - y], fmt="o-")
        plt.xlabel(x_col)
        entries = key if isinstance(key, tuple) else (key,)
        ttl = f"{metric} vs {x_col} | " + ", ".join([f"{c}={v}" for c, v in zip(group_cols, entries)])
        plt.title(ttl)
        plt.tight_layout()
        suffix = "_".join(map(str, entries))
        plt.savefig(outpath.with_name(outpath.stem + f"_{suffix}.png"), dpi=160)
        plt.close()


def main(csv_path=DEFAULT_RESULTS, out_dir=DEFAULT_PLOTS):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(csv_path)
    group_cols = ["g13", "g23", "lam"]
    for metric in ["plv_low_12", "plv_mid_23", "plv_high_13", "pac_low_high_13", "pac_low_mid_12"]:
        outpath = out_dir / f"{metric}_whiskers.png"
        whisker_plot(df, metric, group_cols, x_col="g12", outpath=outpath)


if __name__ == "__main__":
    main()
