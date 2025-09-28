"""
analysis/triad_lock.py
Sliding-window triad phase-lock index:
L(t) = |⟨exp(i(φ1(f1)+φ2(f2)-φ3(f1+f2)))⟩_win|

- Bandpass each channel around target bands.
- Compute instantaneous phases via Hilbert transform.
- Slide a window to estimate time-resolved locking and coherence time.

Also provides a static estimate over full recording.
"""
from __future__ import annotations
import numpy as np
from scipy.signal import butter, filtfilt, hilbert

def _bp(sig, fs, f_lo, f_hi, order=4):
    ny = 0.5*fs
    lo = max(1e-6, f_lo/ny); hi = min(0.999, f_hi/ny)
    b,a = butter(order, [lo,hi], btype="band")
    return filtfilt(b,a,sig)

def triad_phase_lock(sig1, sig2, sig3, fs, f1, f2, bw=1.0):
    x1 = _bp(sig1, fs, f1-bw/2, f1+bw/2)
    y2 = _bp(sig2, fs, f2-bw/2, f2+bw/2)
    z3 = _bp(sig3, fs, (f1+f2)-bw/2, (f1+f2)+bw/2)
    ph = np.angle(hilbert(x1)) + np.angle(hilbert(y2)) - np.angle(hilbert(z3))
    return float(np.abs(np.exp(1j*ph).mean()))

def triad_phase_lock_sliding(sig1, sig2, sig3, fs, f1, f2, bw=1.0, win_s=1.0, step_s=0.25):
    n = len(sig1)
    win = int(win_s*fs); step = int(step_s*fs)
    vals = []
    idxs = []
    for start in range(0, n-win+1, step):
        end = start + win
        vals.append(triad_phase_lock(sig1[start:end], sig2[start:end], sig3[start:end], fs, f1, f2, bw=bw))
        idxs.append((start+end)/2.0/fs)
    return np.array(idxs), np.array(vals)

def coherence_time(idxs, vals, thresh=0.5):
    """
    Return total time where L(t) >= thresh (proxy for lock stability).
    """
    if len(idxs) == 0:
        return 0.0
    dt = np.median(np.diff(idxs)) if len(idxs)>1 else 0.0
    return float((vals >= thresh).sum() * dt)
