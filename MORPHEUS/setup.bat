@echo off
REM MORPHEUS-X Quick Setup Script
REM This script sets up the virtual environment and installs dependencies

setlocal enabledelayedexpansion

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                 MORPHEUS-X Quick Setup                       ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Check if already in project root
if not exist "core\analyzer.py" (
    echo ❌ ERROR: Please run this script from the project root directory!
    echo    cd d:\Project\MORPHEUS
    echo    setup.bat
    pause
    exit /b 1
)

echo ✓ Project root detected: %cd%
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found!
    echo    Install Python 3.7+ from python.org
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Found: %PYTHON_VERSION%
echo.

REM Create virtual environment if not exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Create data folders if not exist
if not exist "data" mkdir data
if not exist "data\uploads" mkdir data\uploads
echo ✓ Data folders ready
echo.

REM Test basic import
echo Testing basic import...
python -c "from core.analyzer import analyze_file; print('✓ Core modules working')" >nul 2>&1
if errorlevel 1 (
    echo ⚠ Warning: Could not import core modules
) else (
    echo ✓ Core modules imported successfully
)
echo.

echo ╔═══════════════════════════════════════════════════════════════╗
echo ║            ✅ Setup Complete!                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo   1. Run tests: python tests\test_static.py
echo   2. Verify system: python setup_and_verify.py
echo   3. Read guide: HOW_TO_RUN.txt or README.md
echo.
echo To return later, activate virtual environment with:
echo   .\.venv\Scripts\activate
echo.
pause
