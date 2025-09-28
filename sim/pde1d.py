"""
sim/pde1d.py
Minimal 1D tri-field PDE integrator.

Model (toy, hyperbolic):
    d2Phi/dt2 = c^2 d2Phi/dx2 - K Phi - Nonlin(Phi) + J(x,t)

- Phi(x,t) is shape (Nx, 3)
- K is 3x3 coupling matrix from TrinityModel
- Nonlin(Phi) = lam * [Phi2*Phi3, Phi1*Phi3, Phi1*Phi2]
- Boundary conditions: Neumann (zero-gradient) by default

CFL stability (rough): c * dt / dx <= 1/sqrt(3) for safety (since 3 fields)
This is a toy; for production, prefer semi-implicit or spectral schemes.
"""
from __future__ import annotations
import numpy as np
from typing import Callable, Tuple, Optional
from model.lagrangian import TrinityModel

DriveFn = Callable[[float, np.ndarray], np.ndarray]  # (t, xgrid) -> (Nx, 3) array

def neumann_pad(arr: np.ndarray) -> np.ndarray:
    """Pad 1D array with copies of edge values for Neumann BCs."""
    pad = np.empty(arr.shape[0]+2, dtype=arr.dtype)
    pad[1:-1] = arr
    pad[0] = arr[0]
    pad[-1] = arr[-1]
    return pad

def laplacian_1d(field: np.ndarray, dx: float) -> np.ndarray:
    """Compute 1D Laplacian with Neumann BCs for each component separately.
    field: shape (Nx,) or (Nx,)
    """
    pad = neumann_pad(field)
    return (pad[:-2] - 2*pad[1:-1] + pad[2:]) / (dx*dx)

def integrate_1d(model: TrinityModel,
                 L: float = 1.0,
                 Nx: int = 200,
                 T: float = 2.0,
                 dt: float = 1e-3,
                 c: float = 1.0,
                 drive: Optional[DriveFn] = None,
                 phi0: Optional[np.ndarray] = None,
                 vel0: Optional[np.ndarray] = None,
                 controller: Optional[Callable[[float, np.ndarray], float]] = None
                 ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Integrate the 1D PDE. Returns (tgrid, xgrid, Phi, Vel)
    Phi has shape (Nt, Nx, 3)
    If controller is provided, it returns a gain g(t) in [0, ..] that scales the drive.
    """
    Nx = int(Nx)
    Nt = int(T/dt)
    x = np.linspace(0.0, L, Nx)
    tgrid = np.linspace(0.0, T, Nt)

    Phi = np.zeros((Nt, Nx, 3), dtype=float)
    Vel = np.zeros_like(Phi)

    if phi0 is not None:
        Phi[0] = phi0
    if vel0 is not None:
        Vel[0] = vel0

    K = model.K_matrix()
    lam = model.lam

    def nonlin(p):
        # p: (Nx, 3)
        out = np.zeros_like(p)
        out[:,0] = p[:,1]*p[:,2]
        out[:,1] = p[:,0]*p[:,2]
        out[:,2] = p[:,0]*p[:,1]
        return lam * out

    # Precompute CFL warning
    cfl = c * dt / (x[1]-x[0])
    if cfl > 0.5:
        print(f"[warn] CFL parameter {cfl:.2f} > 0.5 (toy threshold). Consider reducing dt or c.")

    for k in range(Nt-1):
        t = tgrid[k]

        # Spatial laplacian for each component
        lap = np.zeros((Nx, 3))
        for j in range(3):
            lap[:, j] = laplacian_1d(Phi[k, :, j], dx=x[1]-x[0])

        # Linear coupling term: -K Phi
        lin = -(Phi[k] @ K.T)  # (Nx,3) @ (3,3)

        # Nonlinear
        nl = -nonlin(Phi[k])

        # Drive
        J = np.zeros((Nx, 3))
        if drive is not None:
            base = drive(t, x)
            if controller is not None:
                gain = float(controller(t, Phi[k]))
                base = gain * base
            J = base

        acc = c*c*lap + lin + nl + J
        Vel[k+1] = Vel[k] + dt*acc
        Phi[k+1] = Phi[k] + dt*Vel[k+1]

    return tgrid, x, Phi, Vel
