# MORPHEUS-X Quick Setup Script (PowerShell)
# This script sets up the virtual environment and installs dependencies

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                 MORPHEUS-X Quick Setup                       ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Check if already in project root
if (-not (Test-Path "core\analyzer.py")) {
    Write-Host "❌ ERROR: Please run this script from the project root directory!" -ForegroundColor Red
    Write-Host "   cd d:\Project\MORPHEUS" -ForegroundColor Yellow
    Write-Host "   .\setup.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Project root detected: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python not found!" -ForegroundColor Red
    Write-Host "   Install Python 3.7+ from python.org" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Create virtual environment if not exists
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Create data folders if not exist
if (-not (Test-Path "data")) { mkdir data | Out-Null }
if (-not (Test-Path "data\uploads")) { mkdir data\uploads | Out-Null }
Write-Host "✓ Data folders ready" -ForegroundColor Green
Write-Host ""

# Test basic import
Write-Host "Testing basic import..." -ForegroundColor Cyan
try {
    python -c "from core.analyzer import analyze_file; print('✓ Core modules working')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Core modules imported successfully" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Warning: Could not import core modules" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║            ✅ Setup Complete!                               ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run tests: python tests\test_static.py" -ForegroundColor Yellow
Write-Host "  2. Verify system: python setup_and_verify.py" -ForegroundColor Yellow
Write-Host "  3. Read guide: HOW_TO_RUN.txt or README.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "To return later, activate virtual environment with:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""
