"""
sweeps/focused_sweep.py
Focused parameter sweep over narrowed windows with bootstrap CIs for PLV/PAC.

Results are written under the repository "out" directory so paths remain portable.
"""
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

from model.lagrangian import TrinityModel
from sim.pde1d import integrate_1d
from control.closed_loop import GainController
from analysis.plv_pac import plv, pac_tort

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "out"

OUT = OUT_DIR / "triality_focused_results.csv"


def metrics_center(Phi, dt) -> Dict[str, float]:
    """Compute center-point PLV/PAC metrics consistent with prior scripts."""
    fs = 1.0 / dt
    center = Phi[:, Phi.shape[1] // 2, :]
    low = (0.2, 0.5)
    mid = (40.0, 45.0)
    high = (120.0, 140.0)
    return {
        "plv_low_12": plv(center[:, 0], center[:, 1], fs, *low),
        "plv_mid_23": plv(center[:, 1], center[:, 2], fs, *mid),
        "plv_high_13": plv(center[:, 0], center[:, 2], fs, *high),
        "pac_low_high_13": pac_tort(center[:, 0], center[:, 2], fs, low, high),
        "pac_low_mid_12": pac_tort(center[:, 0], center[:, 1], fs, low, mid),
    }


def bootstrap_time(Phi, dt, B=30, block=None, seed=42) -> Dict[str, Tuple[float, float, float]]:
    """
    Bootstrap CIs for metrics by resampling time indices with replacement.
    If block is provided (int), sample contiguous blocks of that length.
    Returns dict of metric -> (mean, lo95, hi95)
    """
    rng = np.random.default_rng(seed)
    Nt = Phi.shape[0]
    idx_all = np.arange(Nt)

    def sample_indices():
        if block is None or block <= 1:
            return rng.choice(idx_all, size=Nt, replace=True)
        blocks = []
        n_blocks = int(np.ceil(Nt / block))
        for _ in range(n_blocks):
            start = rng.integers(0, max(1, Nt - block))
            blocks.append(np.arange(start, start + block))
        idx = np.concatenate(blocks)[:Nt]
        return idx

    metrics = {
        "plv_low_12": [],
        "plv_mid_23": [],
        "plv_high_13": [],
        "pac_low_high_13": [],
        "pac_low_mid_12": [],
    }

    for _ in range(B):
        idx = sample_indices()
        Phi_b = Phi[idx]
        m = metrics_center(Phi_b, dt)
        for k, v in m.items():
            metrics[k].append(v)

    out = {}
    for k, vals in metrics.items():
        vals = np.array(vals, dtype=float)
        mean = float(vals.mean())
        lo = float(np.quantile(vals, 0.025))
        hi = float(np.quantile(vals, 0.975))
        out[k] = (mean, lo, hi)
    return out


def run(g12_vals=(0.04, 0.05, 0.06), g13_vals=(-0.02, 0.0, 0.02), g23_vals=(-0.02, 0.0, 0.02),
        lam_vals=(0.0, 0.01, 0.02), T=1.5, dt=7.5e-4, Nx=96, amp=0.03,
        discard_s=0.3, B=30, block=None):
    results = []
    for g12 in g12_vals:
        for g13 in g13_vals:
            for g23 in g23_vals:
                for lam in lam_vals:
                    mdl = TrinityModel(omega=(1.0, 3.5, 5.0), g=(g12, g13, g23), lam=lam)
                    controller = GainController(C_target=0.65, kp=0.8, ki=0.1, kd=0.0, gmin=0.0, gmax=1.0)

                    def drive(t, x):
                        return np.column_stack([
                            amp * np.sin(2 * np.pi * 0.3 * t) * np.ones_like(x),
                            amp * np.sin(2 * np.pi * 42.0 * t) * np.ones_like(x),
                            amp * np.sin(2 * np.pi * 131.95 * t) * np.ones_like(x),
                        ])

                    t, x, Phi, Vel = integrate_1d(
                        mdl,
                        L=1.0,
                        Nx=Nx,
                        T=T,
                        dt=dt,
                        c=1.0,
                        drive=drive,
                        controller=controller,
                    )
                    i0 = int(discard_s / dt)
                    Phi_eff = Phi[i0:]

                    m = metrics_center(Phi_eff, dt)
                    cis = bootstrap_time(Phi_eff, dt, B=B, block=block, seed=1337)
                    row = {
                        "g12": g12,
                        "g13": g13,
                        "g23": g23,
                        "lam": lam,
                    }
                    for k, v in m.items():
                        row[k] = v
                    for k, (mean, lo, hi) in cis.items():
                        row[f"{k}_boot_mean"] = mean
                        row[f"{k}_ci_lo"] = lo
                        row[f"{k}_ci_hi"] = hi
                    results.append(row)

    df = pd.DataFrame(results)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print("Wrote:", OUT, "rows:", len(df))
    return OUT


if __name__ == "__main__":
    run()
