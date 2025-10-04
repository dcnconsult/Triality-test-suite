# PowerShell script for Triality v11 replication
# Equivalent to run_replication.sh for Windows

Write-Host "Starting Triality v11 replication..." -ForegroundColor Green

# Run JPC analysis
Write-Host "Running JPC analysis..." -ForegroundColor Yellow
if (Test-Path "data/jpc/jpc_run_15.csv") {
    python analysis/run_jpc.py
} else {
    Write-Host "JPC data not found, skipping JPC analysis" -ForegroundColor Yellow
}

# Run SPDC analysis  
Write-Host "Running SPDC analysis..." -ForegroundColor Yellow
if (Test-Path "data/spdc/spdc_time_tags.json") {
    python analysis/run_timetags.py --path "data/spdc/spdc_time_tags.json" --fs 1000000 --T 0.2 --seglen 4096
} else {
    Write-Host "SPDC data not found, skipping SPDC analysis" -ForegroundColor Yellow
}

# Run bispectrum analysis on synthetic data
Write-Host "Running bispectrum analysis..." -ForegroundColor Yellow
if (Test-Path "data/synthetic/triad_test.csv") {
    python analysis/run_bispec.py --path "data/synthetic/triad_test.csv" --fs 1000 --seglen 4096 --channels "mode1_I,mode2_I,mode3_I"
} else {
    Write-Host "Synthetic data not found, skipping bispectrum analysis" -ForegroundColor Yellow
}

# Generate plots
Write-Host "Generating plots..." -ForegroundColor Yellow
python analysis/run_plots.py

# Generate universality report
Write-Host "Generating universality report..." -ForegroundColor Yellow
python analysis/report_universality.py

# Check if report was generated
if (Test-Path "out/universality_report.md") {
    Write-Host "✅ Replication report generated successfully!" -ForegroundColor Green
    Write-Host "📄 Report available at: out/universality_report.md" -ForegroundColor Cyan
} else {
    Write-Host "❌ Report missing - check for errors above" -ForegroundColor Red
    exit 1
}

Write-Host "🎉 Triality v11 replication completed!" -ForegroundColor Green
