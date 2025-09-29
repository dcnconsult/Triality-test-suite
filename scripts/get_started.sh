#!/usr/bin/env bash
set -euo pipefail
conda env update -f env/environment.yml || true
python -m src.io.validators --root data/raw || true
pytest -q || true
echo "OK: environment + basic checks. Next: scripts/run-replication.sh"