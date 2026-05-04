@echo off
REM MORPHEUS-X GUI Launcher
REM Starts the Streamlit dashboard

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║         MORPHEUS-X GUI Dashboard Launcher                ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo ⚠️  Virtual environment not detected.
    echo Attempting to activate virtual environment...
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ❌ Failed to activate virtual environment.
        echo Please activate manually and run:
        echo   streamlit run app.py
        pause
        exit /b 1
    )
)

echo ✓ Environment ready
echo.
echo 📦 Checking dependencies...

python -m pip check >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Some dependencies may be missing.
    echo Installing requirements...
    pip install -r requirements.txt
)

echo.
echo 🚀 Starting MORPHEUS-X GUI Dashboard...
echo.
echo ℹ️  The dashboard will open in your browser at http://localhost:8501
echo    Press Ctrl+C to stop the server
echo.

streamlit run app.py

pause
