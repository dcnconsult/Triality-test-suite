"""
analysis/plv_pac.py
Utilities to compute PLV (phase-locking value) and PAC (Tort modulation index).
"""
import numpy as np
from scipy.signal import butter, filtfilt, hilbert

def bandpass(data, fs, f_lo, f_hi, order=4):
    ny = 0.5*fs
    lo = max(1e-6, f_lo/ny)
    hi = min(0.999, f_hi/ny)
    b, a = butter(order, [lo, hi], btype='bandpass')
    return filtfilt(b, a, data, axis=0)

def phase(data):
    """Instantaneous phase via Hilbert transform."""
    analytic = hilbert(data, axis=0)
    return np.angle(analytic)

def amplitude_envelope(data):
    """Instantaneous amplitude via Hilbert transform."""
    analytic = hilbert(data, axis=0)
    return np.abs(analytic)

def plv(sig1, sig2, fs, f_lo, f_hi):
    """PLV between two signals in a band."""
    x1 = bandpass(sig1, fs, f_lo, f_hi)
    x2 = bandpass(sig2, fs, f_lo, f_hi)
    ph1 = phase(x1)
    ph2 = phase(x2)
    dphi = np.unwrap(ph1 - ph2)
    return float(np.abs(np.exp(1j*dphi)).mean())

def pac_tort(phase_sig, amp_sig, fs, f_phase, f_amp, n_bins=18):
    """
    Tort modulation index: phase from low band, amplitude envelope from high band.
    Returns MI in [0, ~0.3] typically.
    """
    lp = bandpass(phase_sig, fs, f_phase[0], f_phase[1])
    hp = bandpass(amp_sig, fs, f_amp[0], f_amp[1])
    ph = phase(lp)
    amp = amplitude_envelope(hp)
    # Bin amplitude by phase
    bins = np.linspace(-np.pi, np.pi, n_bins+1)
    idx = np.digitize(ph.ravel(), bins) - 1
    idx = np.clip(idx, 0, n_bins-1)
    mean_amp = np.zeros(n_bins)
    counts = np.zeros(n_bins)
    for i in range(n_bins):
        sel = (idx == i)
        if np.any(sel):
            mean_amp[i] = amp.ravel()[sel].mean()
            counts[i] = sel.sum()
        else:
            mean_amp[i] = 0.0
    # Normalize to probability distribution
    p = mean_amp / (mean_amp.sum() + 1e-12)
    # Modulation index (KL divergence from uniform, normalized by log(n_bins))
    uniform = 1.0/n_bins
    with np.errstate(divide='ignore', invalid='ignore'):
        kl = np.nansum(p * (np.log(p + 1e-12) - np.log(uniform)))
    mi = kl / np.log(n_bins)
    return float(max(0.0, mi))
