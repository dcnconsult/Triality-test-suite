# Replicate v11 (10 minutes)

## Quick Start

```bash
# 1. Setup environment
bash scripts/get_started.sh

# 2. Run full replication
bash scripts/run_replication.sh
```

## Manual Steps

```bash
# Create environment
conda env create -f env/environment.yml
conda activate triality

# Run individual analyses
python analysis/run_jpc.py
python analysis/run_timetags.py
python analysis/run_bispec.py
python analysis/run_plots.py
python analysis/report_universality.py
```

## Expected Outputs

- `reports/v11_universality.md` - Main universality report
- `reports/figures/` - Generated plots and visualizations
- `data/processed/` - Processed analysis results