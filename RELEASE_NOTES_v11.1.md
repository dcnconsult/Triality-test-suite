# Triality Test Suite v11.1 Release Notes

**Release Date:** January 3, 2025  
**Version:** 11.1.0

## Overview

This release focuses on Windows PowerShell compatibility and complete cross-platform testing, ensuring the Triality Test Suite works seamlessly across Windows, Linux, and macOS environments.

## Key Changes

### 🔧 Windows PowerShell Compatibility
- **Fixed module import errors**: Resolved `ModuleNotFoundError` by implementing proper editable install with `pip install -e .`
- **Added PowerShell scripts**: Created `.ps1` equivalents for all bash scripts (`get_started.ps1`, `run_replication.ps1`)
- **Cross-platform module access**: All modules now accessible from any directory after installation
- **Fixed path handling**: Resolved Windows-specific path issues in data loading and output generation

### 🐛 Bug Fixes
- **Synthetic data format**: Fixed column name mismatch between synthetic data generation and JPC batch analysis
- **Data length compatibility**: Adjusted synthetic data duration to match expected segment lengths (4096 samples)
- **NumPy math import**: Fixed `np.math.erf` import error in surrogate analysis
- **Memory optimization**: Reduced SPDC analysis segment length to prevent memory allocation errors

### 📦 Package Management
- **Proper package structure**: Added `__init__.py` files to all modules for correct Python package discovery
- **Updated pyproject.toml**: Enhanced package configuration for cross-platform compatibility
- **Dependency management**: Improved requirements handling for both conda and pip environments

### 🧪 Testing & Validation
- **Complete pipeline testing**: Verified end-to-end workflow from data generation to report creation
- **Cross-platform validation**: Tested on Windows PowerShell, confirmed Linux/macOS compatibility
- **Synthetic data pipeline**: Full JPC and SPDC analysis pipeline working with generated test data
- **Report generation**: Universality reports generated successfully with proper formatting

### 📚 Documentation Updates
- **Windows installation guide**: Added PowerShell-specific installation instructions
- **Cross-platform notes**: Updated README with platform-specific commands
- **Troubleshooting**: Added common Windows-specific issues and solutions
- **API documentation**: Updated version references throughout documentation

## Technical Details

### New Files
- `scripts/get_started.ps1` - Windows PowerShell setup script
- `scripts/run_replication.ps1` - Windows PowerShell replication pipeline
- `data/jpc/jpc_run_15.csv` - JPC test data
- `data/spdc/spdc_time_tags.json` - SPDC test data

### Modified Files
- All `__init__.py` files - Updated version numbers
- `pyproject.toml` - Version bump and package configuration
- `CITATION.cff` - Updated version and release date
- `README.md` - Windows compatibility instructions
- `analysis/synth_triad.py` - Fixed column names and data length
- `analysis/surrogates.py` - Fixed math import
- Documentation files - Version updates

## Installation

### Windows PowerShell
```powershell
# Clone repository
git clone https://github.com/dcn-triality/triality.git
cd triality

# Setup environment
.\scripts\get_started.ps1

# Run replication
.\scripts\run_replication.ps1
```

### Linux/macOS
```bash
# Clone repository
git clone https://github.com/dcn-triality/triality.git
cd triality

# Setup environment
bash scripts/get_started.sh

# Run replication
bash scripts/run_replication.sh
```

## Verification

After installation, verify the setup:
```bash
python run_demo.py
python analysis/synth_triad.py
python analysis/jpc_batch.py
python analysis/run_plots.py
```

Expected output: All commands should complete without errors and generate appropriate output files.

## Breaking Changes

None. This is a backward-compatible release focused on compatibility improvements.

## Migration Guide

No migration required. Existing users can simply update to v11.1.0 for improved Windows compatibility.

## Contributors

- Darryl C. Novotny - Windows compatibility, PowerShell scripts, bug fixes
- Contributors - Cross-platform testing and validation

## Citation

```bibtex
@software{triality_suite_v11_1,
  title  = {Triality Test Suite v11.1},
  author = {Forward Move / KairosIQ Research},
  year   = {2025},
  url    = {https://github.com/dcn-triality/triality}
}
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/dcn-triality/triality/issues
- Email: darryl@thenovotnys.com

---

**Next Release:** v12.0.0 (planned for Q2 2025) - Multi-lab validation and extended platform support
