"""
model/lagrangian.py
Minimal tri-field Lagrangian, linearization, and eigenmode analysis.
"""
from __future__ import annotations
import numpy as np

class TrinityModel:
    """
    Three coupled fields Phi = (Phi1, Phi2, Phi3) with quadratic potential and
    symmetry-breaking cubic term. Units are abstract until mapped by D().
    """
    def __init__(self, omega=(1.0, 3.5, 5.0), g=(0.05, 0.03, 0.02), lam=0.01, a=(0.0,0.0,0.0)):
        self.omega = np.array(omega, dtype=float)  # natural frequencies
        self.g12, self.g13, self.g23 = g          # pairwise couplings
        self.lam = float(lam)                      # cubic coupling
        self.a = np.array(a, dtype=float)          # quadratic offsets for V

    def K_matrix(self) -> np.ndarray:
        """Linear stiffness/coupling matrix K for small oscillations."""
        o1, o2, o3 = self.omega
        g12, g13, g23 = self.g12, self.g13, self.g23
        K = np.array([[o1**2 + self.a[0], g12, g13],
                      [g12, o2**2 + self.a[1], g23],
                      [g13, g23, o3**2 + self.a[2]]], dtype=float)
        return K

    def eigenmodes(self):
        """Return eigenfrequencies (sqrt of eigenvalues) and mode matrix."""
        evals, evecs = np.linalg.eigh(self.K_matrix())
        evals = np.clip(evals, 1e-12, None)
        return np.sqrt(evals), evecs

    def V(self, Phi):
        """Potential energy (quartic omitted in scaffold)."""
        Phi = np.asarray(Phi, dtype=float)
        quad = 0.5 * np.dot(Phi, self.K_matrix() @ Phi)
        cubic = self.lam * (Phi[0] * Phi[1] * Phi[2])
        return quad + cubic

    def map_to_physical(self, Phi):
        """
        Placeholder for dimensional mapping D: fields -> measurable quantities.
        To be fitted once on a restricted training set (see docs/theory.md).
        """
        # Example dummy mapping: mass-like scale ~ norm of Phi
        M = np.linalg.norm(Phi)
        return {"mass_like": M}
