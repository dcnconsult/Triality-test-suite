"""
analysis/surrogates.py
Phase-shuffle surrogates for significance testing of bicoherence peaks.
"""
from __future__ import annotations
import numpy as np
import math

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
    p = 1.0 - 0.5*(1 + math.erf(z/np.sqrt(2)))
    return float(z), float(p), float(mu), float(sd)


def time_reverse(x: np.ndarray) -> np.ndarray:
    """Simple time-reversal surrogate."""
    return np.asarray(x)[::-1].copy()

def block_shuffle(x: np.ndarray, block: int = 1024, seed: int = None) -> np.ndarray:
    """Shuffle contiguous blocks (destroys long-range phase but preserves local structure)."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x)
    n = len(x)
    if block <= 1:
        idx = rng.permutation(n)
        return x[idx]
    blocks = [x[i:i+block] for i in range(0, n, block)]
    rng.shuffle(blocks)
    return np.concatenate(blocks)[:n]
