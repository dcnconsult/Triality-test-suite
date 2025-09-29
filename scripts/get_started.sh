#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Getting started with Triality v11..."

# Create conda environment
echo "📦 Creating conda environment..."
conda env create -f env/environment.yml || conda env update -f env/environment.yml

# Activate environment
echo "🔧 Activating environment..."
conda activate triality

# Run basic tests
echo "🧪 Running basic tests..."
pytest -q || echo "⚠️  Some tests failed - check your data setup"

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "📁 Creating data directory..."
    mkdir -p data/raw data/processed
fi

echo "✅ Environment setup complete!"
echo "📋 Next steps:"
echo "   1. Place your data files in data/raw/"
echo "   2. Run: bash scripts/run_replication.sh"
echo "   3. Check reports/ for generated outputs"