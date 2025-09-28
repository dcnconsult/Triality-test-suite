"""
analysis/run_plots.py
Run the sweep if needed and then create plots.
"""
import os
from sweeps.param_sweep import main as run_sweep
from analysis.plot_sweep import main as plot_main

CSV = "/mnt/data/triality_sweep_results.csv"

def ensure_csv():
    if not os.path.exists(CSV):
        run_sweep()
    return CSV

def main():
    csv_path = ensure_csv()
    plot_main(csv_path=csv_path, out_dir="/mnt/data/plots")
    print("Plots written to /mnt/data/plots")

if __name__ == "__main__":
    main()
