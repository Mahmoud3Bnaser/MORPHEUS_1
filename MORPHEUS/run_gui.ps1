# MORPHEUS-X GUI Launcher (PowerShell)
# Starts the Streamlit dashboard

$ErrorActionPreference = "Continue"
Clear-Host

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "║         MORPHEUS-X GUI Dashboard Launcher                ║" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if running in virtual environment
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not detected." -ForegroundColor Yellow
    Write-Host "Attempting to activate virtual environment..." -ForegroundColor Yellow
    
    $venv_path = ".\.venv\Scripts\Activate.ps1"
    
    if (Test-Path $venv_path) {
        . $venv_path
        Write-Host "✓ Virtual environment activated" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Virtual environment not found at: $venv_path" -ForegroundColor Red
        Write-Host "Please create a virtual environment first:" -ForegroundColor Yellow
        Write-Host "   python -m venv .venv" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "✓ Environment ready" -ForegroundColor Green
Write-Host ""
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan
Write-Host ""

$dep_check = python -m pip check 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Some dependencies may be missing." -ForegroundColor Yellow
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    Write-Host ""
    pip install -r requirements.txt
    Write-Host ""
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "✓ All dependencies installed" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Starting MORPHEUS-X GUI Dashboard..." -ForegroundColor Green
Write-Host ""
Write-Host "ℹ️  The dashboard will open in your browser at http://localhost:8501" -ForegroundColor Cyan
Write-Host "    Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

# Run Streamlit
streamlit run app.py
