"""
sweeps/param_sweep.py
Parameter sweep over couplings to assess phase-locking/entrainment metrics.
Writes CSV with summary measures.
"""
import numpy as np
import pandas as pd
from model.lagrangian import TrinityModel
from model.drive import vector_drive
from sim.pde1d import integrate_1d
from control.closed_loop import GainController

def summary_metrics(Phi):
    """
    Compute simple metrics: per-field RMS and pairwise correlation over time & space.
    Phi: (Nt, Nx, 3)
    """
    rms = np.sqrt((Phi**2).mean(axis=(0,1)))  # (3,)
    # Flatten time & space for corr:
    flat = Phi.reshape(Phi.shape[0]*Phi.shape[1], 3)
    corr = np.corrcoef(flat, rowvar=False)
    return {
        "rms1": float(rms[0]), "rms2": float(rms[1]), "rms3": float(rms[2]),
        "corr12": float(corr[0,1]), "corr13": float(corr[0,2]), "corr23": float(corr[1,2]),
    }

def main():
    results = []
    # Coarse grid over couplings and lambda
    g12_vals = [0.0, 0.02, 0.05]
    g13_vals = [0.0, 0.02, 0.05]
    g23_vals = [0.0, 0.02, 0.05]
    lam_vals = [0.0, 0.01, 0.03]

    for g12 in g12_vals:
        for g13 in g13_vals:
            for g23 in g23_vals:
                for lam in lam_vals:
                    mdl = TrinityModel(omega=(1.0, 3.5, 5.0), g=(g12,g13,g23), lam=lam)
                    controller = GainController(C_target=0.6, kp=0.8, ki=0.1, kd=0.0, gmin=0.0, gmax=1.0)
                    drive = lambda t, x: np.column_stack([
                        0.02*np.sin(2*np.pi*0.3*t)*np.ones_like(x),
                        0.02*np.sin(2*np.pi*42.0*t)*np.ones_like(x),
                        0.02*np.sin(2*np.pi*131.95*t)*np.ones_like(x),
                    ])
                    t,x,Phi,Vel = integrate_1d(mdl, L=1.0, Nx=128, T=0.5, dt=5e-4, c=1.0, drive=drive, controller=controller)
                    met = summary_metrics(Phi[int(0.2/5e-4):])  # discard transient
                    met.update({"g12":g12,"g13":g13,"g23":g23,"lam":lam})
                    results.append(met)

    df = pd.DataFrame(results)
    out = "/mnt/data/triality_sweep_results.csv"
    df.to_csv(out, index=False)
    print("Wrote:", out, "rows:", len(df))

if __name__ == "__main__":
    main()
