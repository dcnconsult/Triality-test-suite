"""
analysis/synth_timetags.py
Generate a tiny synthetic SPDC-like triad in event time-tags.
"""
import json, numpy as np

def gen_triad_events(T=0.2, fs=2000.0, f1=120.0, f2=80.0, intensity=200.0, seed=7):
    """
    Create inhomogeneous Poisson event times for three channels with slow modulation
    at f1 and f2, and the third approximating sum-frequency content.
    """
    rng = np.random.default_rng(seed)
    N = int(T*fs)
    t = np.arange(N)/fs

    # Modulated intensities (positive)
    lam1 = intensity*(1+0.7*np.sin(2*np.pi*f1*t))
    lam2 = intensity*(1+0.7*np.sin(2*np.pi*f2*t))
    lam3 = intensity*(1+0.7*np.sin(2*np.pi*(f1+f2)*t))

    def thin(lam):
        # Thinning to events: probability per bin p ~ lam / fs (small)
        p = np.clip(lam/fs, 0, 0.9)
        draws = rng.random(size=lam.shape)
        idx = np.where(draws < p)[0]
        return (idx/fs).tolist()

    ch_signal = thin(lam1)
    ch_idler  = thin(lam2)
    ch_sum    = thin(lam3)

    return {"ch_signal": ch_signal, "ch_idler": ch_idler, "ch_sum": ch_sum}

if __name__ == "__main__":
    obj = gen_triad_events()
    out = "/mnt/data/spdc_detuned_run_03.json"
    with open(out, "w") as f:
        json.dump(obj, f)
    print("Wrote", out)
