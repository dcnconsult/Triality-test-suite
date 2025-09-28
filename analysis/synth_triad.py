"""
analysis/synth_triad.py
Create a triad-locked synthetic dataset and write CSV.
"""
import numpy as np, pandas as pd

def make_triad(fs=1000.0, T=4.0, f1=42.0, f2=7.0, amps=(1.0,1.0,1.0), noise=0.3, seed=7):
    rng = np.random.default_rng(seed)
    N = int(T*fs)
    t = np.arange(N)/fs
    x = amps[0]*np.sin(2*np.pi*f1*t + 0.1) + noise*rng.standard_normal(N)
    y = amps[1]*np.sin(2*np.pi*f2*t - 0.2) + noise*rng.standard_normal(N)
    z = amps[2]*np.sin(2*np.pi*(f1+f2)*t + 0.3) + noise*rng.standard_normal(N)
    return t, np.stack([x,y,z], axis=1)

if __name__ == "__main__":
    t, X = make_triad()
    import pandas as pd
    df = pd.DataFrame({"time": t, "ch1": X[:,0], "ch2": X[:,1], "ch3": X[:,2]})
    out = "/mnt/data/triad_test.csv"
    df.to_csv(out, index=False)
    print("Wrote", out)
