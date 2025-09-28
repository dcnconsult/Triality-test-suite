"""
cosmo/toy.py
Toy Poisson solver with an "informational" density rho_I(x) contribution.
"""
import numpy as np

def poisson_1d(rho, dx):
    """
    Solve d2phi/dx2 = rho with zero-Dirichlet BCs (toy) using finite differences.
    """
    n = len(rho)
    A = np.zeros((n,n))
    b = rho.copy()
    for i in range(n):
        A[i,i] = -2.0
        if i>0: A[i,i-1] = 1.0
        if i<n-1: A[i,i+1] = 1.0
    # Zero BCs already encoded if we leave edges as is.
    phi = np.linalg.solve(A/(dx*dx), b)
    return phi

def demo():
    x = np.linspace(0,1,400)
    dx = x[1]-x[0]
    # baryonic bump + informational tail
    rho_b = np.exp(-((x-0.4)/0.05)**2)
    rho_I = 0.3/(1+((x-0.7)/0.1)**2)
    phi = poisson_1d(rho_b+rho_I, dx)
    return x, phi, rho_b, rho_I

if __name__ == "__main__":
    x, phi, rb, rI = demo()
    print("Toy potential summary:", float(np.min(phi)), float(np.max(phi)))
