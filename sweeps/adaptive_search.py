"""
sweeps/adaptive_search.py
Adaptive search for PLV/PAC "hotspots." Starts from an existing sweep CSV,
ranks configurations by a composite objective, and explores local neighborhoods
with finer steps. Writes a new CSV and a ranked summary under the repository "out" directory.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from model.lagrangian import TrinityModel
from sim.pde1d import integrate_1d
from control.closed_loop import GainController
from analysis.plv_pac import plv, pac_tort

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "out"

OUT = OUT_DIR / "triality_adaptive_results.csv"
RANK = OUT_DIR / "triality_adaptive_ranked.csv"
DEFAULT_SEED = OUT_DIR / "triality_sweep_results.csv"


def objective(row, w_plv=1.0, w_pac=1.0):
    plv_sum = row["plv_low_12"] + row["plv_mid_23"] + row["plv_high_13"]
    pac_sum = row["pac_low_high_13"] + row["pac_low_mid_12"]
    return w_plv * plv_sum + w_pac * pac_sum


def metrics_from_sim(Phi, dt):
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


def explore_local(seed, steps=(0.01, 0.01, 0.01, 0.01), span=2):
    g12c, g13c, g23c, lamc = seed
    g12_range = [g12c + i * steps[0] for i in range(-span, span + 1)]
    g13_range = [g13c + i * steps[1] for i in range(-span, span + 1)]
    g23_range = [g23c + i * steps[2] for i in range(-span, span + 1)]
    lam_range = [max(0.0, lamc + i * steps[3]) for i in range(-span, span + 1)]
    return g12_range, g13_range, g23_range, lam_range


def run(csv_seed=DEFAULT_SEED, top_k=3, span=1, steps=(0.01, 0.01, 0.01, 0.01),
        T=0.5, dt=1e-3, amp=0.04, Nx=64):
    csv_seed = Path(csv_seed)
    df = pd.read_csv(csv_seed)
    df = df.copy()
    df["objective"] = df.apply(objective, axis=1)
    ranked = df.sort_values("objective", ascending=False)

    RANK.parent.mkdir(parents=True, exist_ok=True)
    ranked.to_csv(RANK, index=False)

    seeds = ranked.head(top_k)[["g12", "g13", "g23", "lam"]].values.tolist()

    results = []
    for g12c, g13c, g23c, lamc in seeds:
        g12_range, g13_range, g23_range, lam_range = explore_local((g12c, g13c, g23c, lamc), steps=steps, span=span)
        for g12 in g12_range:
            for g13 in g13_range:
                for g23 in g23_range:
                    for lam in lam_range:
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
                        i0 = int(0.25 / dt)
                        Phi_eff = Phi[i0:]
                        met = metrics_from_sim(Phi_eff, dt)
                        met.update({"g12": g12, "g13": g13, "g23": g23, "lam": lam})
                        met["objective"] = objective(pd.Series(met))
                        results.append(met)

    out_df = pd.DataFrame(results)
    out_df.sort_values("objective", ascending=False, inplace=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(OUT, index=False)
    print("Wrote:", OUT, "rows:", len(out_df))
    print("Ranked seed table:", RANK)
    return OUT, RANK


if __name__ == "__main__":
    run()
