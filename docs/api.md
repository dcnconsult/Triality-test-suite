API Overview
CLI

triality.py run --target {jpc,spdc,cross} --config <yaml> --outdir <dir> [--seed 1337]

triality.py report --inputs <dir1> <dir2> --config configs/report_v11.yaml --outdir reports/

Key Modules

src/dsp/bispectrum.py — bispectrum & bicoherence

src/triad/hotspot_scan.py — triad grid search & constraints

src/pipelines/* — end-to-end runs