# Triality: From Informational Triples to Tri-Field Physics

> Draft repo scaffold • 2025-09-28

This repository hosts a **falsifiable** research program that turns the Triality vision
into operational math, simulations, and preregistered experiments.

## Minimal thesis

- **Axiom A (informational microstate).** Physical reality emerges from discrete informational states labeled by integer triples \(s=(x,y,z)\in\mathbb{Z}^3\) constrained by \(x^3+y^3+z^3-k=0\).
- **Axiom B (coarse-graining).** Continuum fields \(\Phi_j\) arise as moments of local solution densities over integer neighborhoods.
- **Axiom C (dynamics).** Dynamics follow a tri-field Lagrangian with explicit couplings and symmetry-breaking terms; measurable quantities are carried by \(\Phi\), not raw integers.

## Repo layout

```
model/        # Lagrangian, coarse-graining, drive coupling, parameter sets
sim/          # Eigenmode analysis, PDE integrator (FDM prototype), sweep tools
neuro/        # Preregistered EEG protocol and dosimetry worksheets
analysis/     # Stats pipelines and power-analysis helpers
cosmo/        # Toy Poisson solver with informational density rho_I
docs/         # Design notes, theory sketch, kill-switch criteria
.github/      # CI hooks (lint, smoke tests) - placeholder
```

## Quickstart

```bash
python run_demo.py
```

This prints the eigen-frequencies of the linearized tri-field system and runs a small
time-domain integration to illustrate phase locking under a tri-tone drive.

## Scientific discipline

We operate with **kill-switches**:
- **K1 (EEG).** No effects beyond sham after two replications ⇒ retire SR/entrainment pillar.
- **K2 (nuclear).** Cannot reproduce magic closures within ±1 without >3 tuned constants ⇒ retire harmony claim.
- **K3 (cosmo).** Cannot match a rotation curve with comparable parameter count ⇒ retire dark-matter rhetoric until math improves.

See `docs/discipline.md`.


## New: 1D PDE + Closed Loop + Sweeps

Run a 1D PDE demo with closed-loop gain (simulated C_m):

```bash
python -m sweeps.param_sweep
```

This writes `triality_sweep_results.csv` with RMS and correlation summaries across coupling grids.
