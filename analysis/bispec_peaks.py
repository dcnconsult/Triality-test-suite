"""
analysis/bispec_peaks.py
Utilities to extract bicoherence peaks and estimate dominant mode frequencies.
"""
from __future__ import annotations
import numpy as np
from numpy.fft import rfft, rfftfreq

def dominant_freq(sig: np.ndarray, fs: float, nmax: int = 3):
    """Return top-nmax peak frequencies from magnitude spectrum (rough)."""
    sig = np.asarray(sig, dtype=float)
    F = rfft(sig * np.hanning(len(sig)))
    mag = np.abs(F)
    f = rfftfreq(len(sig), 1.0/fs)
    # ignore DC
    mag[0] = 0.0
    idx = np.argsort(mag)[::-1][:nmax]
    return f[idx], mag[idx]

def find_bicoherence_peak(b2: np.ndarray, f: np.ndarray):
    """Return peak location and value in bicoherence matrix."""
    idx = np.unravel_index(np.argmax(b2), b2.shape)
    i, j = int(idx[0]), int(idx[1])
    f1, f2 = float(f[i]), float(f[j])
    val = float(b2[i,j])
    return {"f1": f1, "f2": f2, "b2_peak": val, "i": i, "j": j}
