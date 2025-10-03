"""
sweeps/param_sweep.py
Parameter sweep over couplings to assess entrainment metrics (PLV/PAC) + RMS/corr.
Writes CSV with summary measures under the repository "out" directory.
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
OUT = OUT_DIR / "triality_sweep_results.csv"


def summary_metrics(Phi, fs):
    """
    Compute metrics:
      - per-field RMS
      - pairwise correlation (flattened)
      - PLV in three bands (low ~ drive1, mid ~ drive2, high ~ drive3)
      - PAC: low-phase x high-amp (1x3), low-phase x mid-amp (1x2)
    Phi: (Nt, Nx, 3)
    """
    rms = np.sqrt((Phi**2).mean(axis=(0, 1)))
    flat = Phi.reshape(Phi.shape[0] * Phi.shape[1], 3)
    corr = np.corrcoef(flat, rowvar=False)

    center = Phi[:, Phi.shape[1] // 2, :]
    low = (0.2, 0.5)
    mid = (40.0, 45.0)
    high = (120.0, 140.0)

    plv_l_12 = plv(center[:, 0], center[:, 1], fs, *low)
    plv_m_23 = plv(center[:, 1], center[:, 2], fs, *mid)
    plv_h_13 = plv(center[:, 0], center[:, 2], fs, *high)

    pac_lh_13 = pac_tort(center[:, 0], center[:, 2], fs, low, high)
    pac_lm_12 = pac_tort(center[:, 0], center[:, 1], fs, low, mid)

    return {
        "rms1": float(rms[0]),
        "rms2": float(rms[1]),
        "rms3": float(rms[2]),
        "corr12": float(corr[0, 1]),
        "corr13": float(corr[0, 2]),
        "corr23": float(corr[1, 2]),
        "plv_low_12": float(plv_l_12),
        "plv_mid_23": float(plv_m_23),
        "plv_high_13": float(plv_h_13),
        "pac_low_high_13": float(pac_lh_13),
        "pac_low_mid_12": float(pac_lm_12),
    }


def main():
    results = []
    g12_vals = [0.0, 0.02, 0.05]
    g13_vals = [0.0, 0.02, 0.05]
    g23_vals = [0.0, 0.02, 0.05]
    lam_vals = [0.0, 0.01, 0.03]

    for g12 in g12_vals:
        for g13 in g13_vals:
            for g23 in g23_vals:
                for lam in lam_vals:
                    mdl = TrinityModel(omega=(1.0, 3.5, 5.0), g=(g12, g13, g23), lam=lam)
                    controller = GainController(C_target=0.6, kp=0.8, ki=0.1, kd=0.0, gmin=0.0, gmax=1.0)

                    def drive(t, x):
                        return np.column_stack([
                            0.02 * np.sin(2 * np.pi * 0.3 * t) * np.ones_like(x),
                            0.02 * np.sin(2 * np.pi * 42.0 * t) * np.ones_like(x),
                            0.02 * np.sin(2 * np.pi * 131.95 * t) * np.ones_like(x),
                        ])

                    dt = 5e-4
                    T = 0.8
                    t, x, Phi, Vel = integrate_1d(
                        mdl,
                        L=1.0,
                        Nx=128,
                        T=T,
                        dt=dt,
                        c=1.0,
                        drive=drive,
                        controller=controller,
                    )

                    i0 = int(0.2 / dt)
                    Phi_eff = Phi[i0:]

                    met = summary_metrics(Phi_eff, fs=1.0 / dt)
                    met.update({"g12": g12, "g13": g13, "g23": g23, "lam": lam})
                    results.append(met)

    df = pd.DataFrame(results)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print("Wrote:", OUT, "rows:", len(df))


if __name__ == "__main__":
    main()
