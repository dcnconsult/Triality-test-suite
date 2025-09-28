"""
control/closed_loop.py
Closed-loop controller stub for C_m (consciousness coherence index).

We simulate C_m as a function of Phi using a simple observable:
    C_m(t) = sigmoid( w1*RMS(Phi[:,0]) + w2*RMS(Phi[:,1]) + w3*RMS(Phi[:,2]) - bias )

The controller returns a gain g(t) that scales the external drive, aiming to keep
C_m near a target setpoint C_target.
"""
from __future__ import annotations
import numpy as np

def cm_index(Phi_slice: np.ndarray, weights=(0.5, 0.3, 0.2), bias=0.3) -> float:
    """
    Phi_slice: (Nx, 3) at time t
    Returns simulated C_m in [0,1]
    """
    rms = np.sqrt((Phi_slice**2).mean(axis=0))
    z = (weights[0]*rms[0] + weights[1]*rms[1] + weights[2]*rms[2]) - bias
    return 1.0/(1.0 + np.exp(-4.0*z))

class GainController:
    def __init__(self, C_target=0.6, kp=1.0, ki=0.0, kd=0.0, gmin=0.0, gmax=1.0):
        self.C_target = float(C_target)
        self.kp, self.ki, self.kd = float(kp), float(ki), float(kd)
        self.e_int = 0.0
        self.e_prev = 0.0
        self.gmin, self.gmax = float(gmin), float(gmax)

    def __call__(self, t: float, Phi_slice: np.ndarray) -> float:
        C = cm_index(Phi_slice)
        e = self.C_target - C
        de = e - self.e_prev
        self.e_int += e
        self.e_prev = e
        g = self.kp*e + self.ki*self.e_int + self.kd*de
        return float(np.clip(g, self.gmin, self.gmax))
