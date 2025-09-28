"""
model/drive.py
Exogenous drive constructors: narrowband, tri-tone, SR-like envelopes.
"""
from __future__ import annotations
import numpy as np

def tri_tone(t, amps=(0.02, 0.02, 0.02), freqs=(0.3, 42.0, 131.95), phase=(0.0,0.0,0.0)):
    """Time-domain tri-tone drive (scalar); units arbitrary here."""
    a1,a2,a3 = amps
    f1,f2,f3 = freqs
    p1,p2,p3 = phase
    return a1*np.sin(2*np.pi*f1*t + p1) + a2*np.sin(2*np.pi*f2*t + p2) + a3*np.sin(2*np.pi*f3*t + p3)

def vector_drive(t, amps3=((0.02,0,0),(0,0.02,0),(0,0,0.02)), freqs=(0.3,42.0,131.95)):
    """
    Drive each field with one tone (diagonal coupling) for clarity.
    Returns shape (3,) array.
    """
    d = np.zeros(3)
    for i in range(3):
        amp_vec = np.array(amps3[i])
        if amp_vec[i] != 0:
            d[i] = amp_vec[i] * np.sin(2*np.pi*freqs[i]*t)
    return d
