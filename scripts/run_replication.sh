#!/usr/bin/env bash
set -euo pipefail
python -m src.pipelines.jpc_pipeline --config configs/jpc_v11.yaml --outdir data/processed/jpc_v11
python -m src.pipelines.spdc_pipeline --config configs/spdc_v11.yaml --outdir data/processed/spdc_v11
python -m src.pipelines.cross_platform --jpc data/processed/jpc_v11 --spdc data/processed/spdc_v11 \
--config configs/report_v11.yaml --outdir reports/
(test -f reports/v11_universality.md && echo "Replication report generated.") || \
(echo "Report missing" && exit 1)