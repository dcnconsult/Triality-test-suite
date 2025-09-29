#!/usr/bin/env bash
set -euo pipefail

echo "Starting Triality v11 replication..."

# Run JPC analysis
echo "Running JPC analysis..."
python analysis/run_jpc.py

# Run SPDC analysis
echo "Running SPDC analysis..."
python analysis/run_timetags.py

# Run bispectrum analysis
echo "Running bispectrum analysis..."
python analysis/run_bispec.py

# Generate plots
echo "Generating plots..."
python analysis/run_plots.py

# Generate universality report
echo "Generating universality report..."
python analysis/report_universality.py

# Check if report was generated
if [ -f "reports/v11_universality.md" ]; then
    echo "✅ Replication report generated successfully!"
    echo "📄 Report available at: reports/v11_universality.md"
else
    echo "❌ Report missing - check for errors above"
    exit 1
fi

echo "🎉 Triality v11 replication completed!"