"""
analysis/bispectrum.py
Bispectrum and bicoherence estimators.
"""
from __future__ import annotations
import numpy as np
from numpy.fft import rfft, rfftfreq
from typing import Optional, Tuple

def _segment(data: np.ndarray, seglen: int, step: Optional[int]=None):
    x = np.asarray(data, dtype=float)
    if step is None:
        step = seglen//2
    nseg = 1 + max(0, (len(x)-seglen)//step)
    out = np.empty((nseg, seglen), dtype=float)
    for i in range(nseg):
        s = i*step
        out[i] = x[s:s+seglen]
    return out

def bispectrum(x: np.ndarray, fs: float, seglen: int, step: Optional[int]=None, detrend: bool=True):
    x = np.asarray(x, dtype=float)
    X = _segment(x - (x.mean() if detrend else 0.0), seglen, step)
    win = np.hanning(seglen)[None, :]
    F = rfft(X*win, axis=1)
    nF = F.shape[1]
    S3 = np.zeros((nF, nF), dtype=complex)
    S2 = np.zeros((nF, nF), dtype=float)
    for row in F:
        for i in range(nF):
            for j in range(nF):
                k = i + j
                if k < nF:
                    S3[i,j] += row[i]*row[j]*np.conj(row[k])
                    S2[i,j] += (np.abs(row[i])*np.abs(row[j])*np.abs(row[k]))
    S3 /= F.shape[0]
    S2 /= F.shape[0] + 1e-12
    f = rfftfreq(seglen, d=1.0/fs)
    b2 = (np.abs(S3)**2) / ((S2**2)+1e-20)
    return f, S3, b2

def cross_bispectrum(x: np.ndarray, y: np.ndarray, z: np.ndarray, fs: float, seglen: int, step: Optional[int]=None):
    from numpy.fft import rfft
    Xs = _segment(x - np.mean(x), seglen, step)
    Ys = _segment(y - np.mean(y), seglen, step)
    Zs = _segment(z - np.mean(z), seglen, step)
    win = np.hanning(seglen)[None, :]
    FX = rfft(Xs*win, axis=1); FY = rfft(Ys*win, axis=1); FZ = rfft(Zs*win, axis=1)
    nF = FX.shape[1]
    S3 = np.zeros((nF, nF), dtype=complex)
    S2 = np.zeros((nF, nF), dtype=float)
    for a,b,c in zip(FX,FY,FZ):
        for i in range(nF):
            for j in range(nF):
                k = i + j
                if k < nF:
                    S3[i,j] += a[i]*b[j]*np.conj(c[k])
                    S2[i,j] += (np.abs(a[i])*np.abs(b[j])*np.abs(c[k]))
    S3 /= FX.shape[0]
    S2 /= FX.shape[0] + 1e-12
    f = rfftfreq(seglen, d=1.0/(fs))
    b2 = (np.abs(S3)**2) / ((S2**2)+1e-20)
    return f, S3, b2
