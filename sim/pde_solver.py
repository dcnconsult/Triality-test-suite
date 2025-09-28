"""
sim/pde_solver.py
Simple time-domain integrator for the tri-field ODE at a single spatial point.
This is a scaffold: PDE/FEM grid support can be added later.
"""
from __future__ import annotations
import numpy as np
from model.lagrangian import TrinityModel

def integrate(model: TrinityModel, T=5.0, dt=1e-3, drive=None, y0=None):
    """
    Integrate second-order system: phi_ddot + K phi + nonlinear = J(t)
    Using explicit Verlet-like scheme for demonstration.
    """
    N = int(T/dt)
    phi = np.zeros((N,3))
    vel = np.zeros((N,3))
    if y0 is not None:
        phi[0] = y0.get("phi", np.zeros(3))
        vel[0] = y0.get("vel", np.zeros(3))

    K = model.K_matrix()
    lam = model.lam

    def nonlin(p):
        return lam * np.array([p[1]*p[2], p[0]*p[2], p[0]*p[1]])

    for k in range(N-1):
        t = k*dt
        J = np.zeros(3)
        if drive is not None:
            J = np.asarray(drive(t))
        acc = -K @ phi[k] - nonlin(phi[k]) + J
        vel[k+1] = vel[k] + dt*acc
        phi[k+1] = phi[k] + dt*vel[k+1]
    tgrid = np.linspace(0, T, N)
    return tgrid, phi, vel
