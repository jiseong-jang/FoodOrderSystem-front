@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo Starting FastAPI Voice Order Server...
echo ========================================
echo.

REM Check if Python is available
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot find Python.
    echo.
    echo Please check if Python is installed.
    echo Download Python: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check Python version
python --version
if errorlevel 1 (
    echo ERROR: Failed to check Python version
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment
        echo Please check if Python is installed correctly.
        echo.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install required packages
echo Checking and installing packages...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

REM Start server
echo.
echo ========================================
echo Starting server... (Port 5001)
echo ========================================
echo.
echo Open http://localhost:5001 in your browser.
echo Press Ctrl+C to stop the server.
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 5001

pause

