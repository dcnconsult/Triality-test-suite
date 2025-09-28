"""
run_demo.py
Quick smoke test: eigenmodes + short integration.
"""
from model.lagrangian import TrinityModel
from model.drive import vector_drive
from sim.pde_solver import integrate

def main():
    mdl = TrinityModel(omega=(1.0, 3.5, 5.0), g=(0.05, 0.03, 0.02), lam=0.01)
    freqs, modes = mdl.eigenmodes()
    print("Eigen-frequencies (arb. units):", [round(float(f), 5) for f in freqs])
    t, phi, vel = integrate(mdl, T=2.0, dt=1e-3, drive=lambda tt: vector_drive(tt))
    print("Integration finished; phi rms:", (phi**2).mean(axis=0)**0.5)

if __name__ == "__main__":
    main()
