# PowerShell script for getting started with Triality v11
# Equivalent to get_started.sh for Windows

Write-Host "Getting started with Triality v11..." -ForegroundColor Green

# Check if conda is available
$condaAvailable = Get-Command conda -ErrorAction SilentlyContinue
if ($condaAvailable) {
    # Create conda environment
    Write-Host "Creating conda environment..." -ForegroundColor Yellow
    conda env create -f env/environment.yml
    if ($LASTEXITCODE -ne 0) {
        conda env update -f env/environment.yml
    }
    
    # Activate environment
    Write-Host "Activating environment..." -ForegroundColor Yellow
    conda activate triality
} else {
    Write-Host "Conda not found. Using pip instead..." -ForegroundColor Yellow
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r env/requirements.txt
    pip install -e .
}

# Run basic tests
Write-Host "Running basic tests..." -ForegroundColor Yellow
python run_demo.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Demo test failed - check your setup" -ForegroundColor Red
}

# Check if data directory exists
if (-not (Test-Path "data")) {
    Write-Host "Creating data directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "data" -Force
    New-Item -ItemType Directory -Path "data\raw" -Force
    New-Item -ItemType Directory -Path "data\processed" -Force
}

# Generate synthetic test data
Write-Host "Generating synthetic test data..." -ForegroundColor Yellow
python analysis/synth_triad.py

Write-Host "Environment setup complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "   1. Place your data files in data/raw/" -ForegroundColor White
Write-Host "   2. Run: .\scripts\run_replication.ps1" -ForegroundColor White
Write-Host "   3. Check out directory for generated outputs" -ForegroundColor White