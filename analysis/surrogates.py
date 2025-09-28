"""
analysis/surrogates.py
Phase-shuffle surrogates for significance testing of bicoherence peaks.
"""
from __future__ import annotations
import numpy as np

def phase_randomize(x: np.ndarray, seed: int=None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    X = np.fft.rfft(x)
    ph = np.exp(1j * rng.uniform(0, 2*np.pi, size=X.shape))
    Xs = np.abs(X) * ph
    xs = np.fft.irfft(Xs, n=len(x))
    return xs

def peak_zscore(peak_val: float, null_vals: list[float]):
    null = np.asarray(null_vals, dtype=float)
    mu = null.mean()
    sd = null.std(ddof=1) + 1e-12
    z = (peak_val - mu)/sd
    p = 1.0 - 0.5*(1 + np.math.erf(z/np.sqrt(2)))
    return float(z), float(p), float(mu), float(sd)
