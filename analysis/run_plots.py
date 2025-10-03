"""
analysis/run_plots.py
Run the sweep if needed and then create plots.
"""
from pathlib import Path

from sweeps.param_sweep import main as run_sweep
from analysis.plot_sweep import main as plot_main

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "out"

CSV = OUT_DIR / "triality_sweep_results.csv"
PLOT_DIR = OUT_DIR / "plots"


def ensure_csv():
    if not CSV.exists():
        run_sweep()
    return CSV


def main():
    csv_path = ensure_csv()
    plot_dir = PLOT_DIR
    plot_dir.mkdir(parents=True, exist_ok=True)
    plot_main(csv_path=csv_path, out_dir=plot_dir)
    print("Plots written to", plot_dir)


if __name__ == "__main__":
    main()
