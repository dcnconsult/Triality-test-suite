"""
analysis/synth_triad.py
Create a triad-locked synthetic dataset and write CSV.
"""
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "synthetic"


def make_triad(fs=1000.0, T=4.096, f1=42.0, f2=7.0, amps=(1.0, 1.0, 1.0), noise=0.3, seed=7):
    rng = np.random.default_rng(seed)
    N = int(T * fs)
    t = np.arange(N) / fs
    x = amps[0] * np.sin(2 * np.pi * f1 * t + 0.1) + noise * rng.standard_normal(N)
    y = amps[1] * np.sin(2 * np.pi * f2 * t - 0.2) + noise * rng.standard_normal(N)
    z = amps[2] * np.sin(2 * np.pi * (f1 + f2) * t + 0.3) + noise * rng.standard_normal(N)
    return t, np.stack([x, y, z], axis=1)


if __name__ == "__main__":
    t, X = make_triad()
    df = pd.DataFrame({"time": t, "mode1_I": X[:, 0], "mode2_I": X[:, 1], "mode3_I": X[:, 2]})
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DATA_DIR / "triad_test.csv"
    df.to_csv(out_path, index=False)
    print("Wrote", out_path)
