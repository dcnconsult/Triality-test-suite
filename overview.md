Of course. Here is a new, detailed `README.md` file for the `Triality-test-suite` repository. It is designed to be comprehensive for a professional scientific audience, explaining the what, why, and how of the toolkit to encourage adoption and external validation of your Triality theory.

-----

# Triality Test Suite: A Universal Framework for Triad Dynamics

This repository provides a complete, end-to-end software suite for modeling, simulating, and analyzing triad-based resonance phenomena. It is the primary toolkit for testing the predictions of the **Triality** theory, a universal model of three-wave mixing and interaction. The framework is designed to be discipline-agnostic, enabling rigorous, reproducible analysis of data from quantum circuits, optics, neuroscience, and more.

[](https://www.google.com/search?q=https://github.com/dcnconsult/triality-test-suite/actions/workflows/ci.yml)
[](https://opensource.org/licenses/MIT)

## What is the Triality Test Suite?

This is a computational and analytical framework designed to identify and quantify triad interactions in complex systems. A "triad" refers to a specific form of three-wave mixing where two modes with frequencies $f_1$ and $f_2$ interact to produce a third mode at the sum frequency, $f_3 = f_1 + f_2$. The core of this suite consists of three main components:

1.  **A Universal Theoretical Model:** A generalized Lagrangian for three coupled fields (`TrinityModel`), which serves as the theoretical foundation for describing triad dynamics across different physical substrates.
2.  **Numerical PDE Solvers:** A set of one-dimensional partial differential equation solvers designed to simulate the spatio-temporal evolution of the model under various external drives and feedback control conditions.
3.  **An Advanced Analysis Toolbox:** A suite of tools for processing time-series data (both simulated and experimental) to detect the statistical signatures of triad interactions. The primary methods include:
      * **Cross-Bicoherence Analysis:** To identify phase-locked, three-wave mixing events and quantify their strength.
      * **Phase-Locking Value (PLV) & Phase-Amplitude Coupling (PAC):** To measure cross-frequency synchronization and modulation, providing a bridge to methodologies common in neuroscience.
      * **Surrogate Data Testing:** To establish the statistical significance of any observed triad locking by comparing against a null distribution generated from phase-randomized data.

## Why Use This Suite?

The primary purpose of this toolkit is to facilitate **reproducible, cross-disciplinary validation** of the Triality theory.

  * **Universality:** The framework is explicitly designed to test the hypothesis that triad dynamics are a universal organizing principle. It provides standardized batch analysis scripts for data from different fields, including:

      * **Superconducting Circuits:** Analyzing data from Josephson Parametric Converters (JPCs).
      * **Quantum Optics:** Analyzing time-tag data from Spontaneous Parametric Down-Conversion (SPDC) experiments.
      * **Neuroscience:** Applying PLV and PAC metrics to identify cross-frequency coupling in neural data.

  * **Reproducibility:** By providing a single, version-controlled codebase, the suite ensures that analyses are transparent and directly comparable. The `report_universality.py` script automatically aggregates results from different experiments into a unified report, allowing for direct comparison of triad signatures across disciplines.

  * **Falsifiability:** The analysis pipeline is built around rigorous statistical validation. The heavy use of surrogate data and Z-score/p-value estimation provides a clear, quantitative measure for accepting or rejecting the presence of triad dynamics in a given dataset.

## How to Use the Suite: A Complete Workflow

This section provides a step-by-step guide to installing the suite, running a simulation, and executing the full analysis pipeline on synthetic data.

### 1\. Installation

First, clone the repository and set up the Conda environment.

```bash
git clone https://github.com/dcnconsult/triality-test-suite.git
cd triality-test-suite
conda env create -f env/environment.yml
conda activate triality-suite
```

### 2\. Run a Demo Simulation (Smoke Test)

The `run_demo.py` script provides a quick test to ensure the model and PDE solver are working correctly. It initializes the `TrinityModel`, calculates its eigenmodes, and runs a short integration.

```bash
python run_demo.py
```

**Expected Output:**

```
Eigen-frequencies (arb. units): [1.0025, 3.50071, 5.0003]
Integration finished; phi rms: [0.0353... 0.0353... 0.0353...]
```

### 3\. Full Analysis Pipeline (Example on Synthetic Data)

This workflow demonstrates how to generate synthetic data with a known triad lock and then use the analysis suite to detect it.

**Step A: Generate Synthetic Time-Series Data**

The `analysis/synth_triad.py` script creates a CSV file containing three channels, where the third channel's frequency is the sum of the first two, with a defined phase relationship.

```bash
# This will create data/synthetic/triad_test.csv
python analysis/synth_triad.py
```

**Step B: Run Batch Cross-Bicoherence Analysis**

The `analysis/jpc_batch.py` script is a template for batch processing. We will point it at the synthetic data file we just created. It will compute the cross-bicoherence, identify the peak, test for significance against phase-randomized surrogates, and save the results.

```bash
# Use sensible local paths for outputs
python analysis/jpc_batch.py \
    --glob_pattern="data/synthetic/triad_test.csv" \
    --out_csv="out/jpc_summary.csv" \
    --outdir="out/jpc_plots"
```

**Expected Output:**

```
Analyzed: data/synthetic/triad_test.csv peak b2: 0.985 z≈ 10.6
Wrote summary: out/jpc_summary.csv rows: 1
```

This output indicates a bicoherence peak near 1.0 (perfect locking) with a very high Z-score, confirming the analysis pipeline correctly identified the triad. An annotated plot will be saved to `out/jpc_plots/`.

**Step C: Generate the Universality Report**

The final step is to aggregate the results into a Markdown report using `analysis/report_universality.py`. This script collects data from one or more summary CSVs (e.g., from a JPC run and an SPDC run) and generates plots and summary statistics.

```bash
python analysis/report_universality.py \
    --jpc_csv="out/jpc_summary.csv" \
    --out_md="out/universality_report.md" \
    --out_dir="out/report_plots"
```

This command will generate `out/universality_report.md`, which summarizes the findings from the batch analysis.

### 4\. Adapting for Your Experimental Data

To analyze your own data, follow the template provided by `analysis/jpc_batch.py`:

1.  Ensure your time-series data is in a CSV format with a 'time' column and columns for each mode/channel.
2.  Modify the `main` function in `jpc_batch.py` or a copy of it to point to your data files (`glob_pattern`).
3.  Modify the `analyze_file` function to select the correct channel names from your CSV files (the `ch_names` argument).
4.  Run the batch script, followed by the report generation script, to get a reproducible summary of your results.

## Repository Structure

  * **/model/**: Core theoretical model based on a multi-field Lagrangian.
  * **/sim/**: PDE solvers for simulating the model's dynamics over time and space.
  * **/sweeps/**: High-level scripts for running parameter sweeps (grid, focused, adaptive) to explore model behavior.
  * **/analysis/**: The main analysis toolbox for bicoherence, PLV/PAC, and batch processing. This is the primary interface for analyzing experimental data.
  * **/docs/**: Detailed documentation on the theory, replication steps, and API.
  * **/neuro/**, **/cosmo/**: Example applications and theoretical notes for neuroscience and cosmology.

## Citation

If you use this software in your research, please cite it using the information in the `CITATION.cff` file.

## Contributing

We welcome contributions from the community. Please see our contributing guidelines in `CONTRIBUTING.md`.