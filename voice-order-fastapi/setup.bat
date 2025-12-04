@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo Setting up FastAPI Voice Order Server...
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

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    echo Please check if Python is installed correctly.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install packages
echo Installing packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the server, run:
echo   start.bat
echo.
echo Or manually:
echo   call .venv\Scripts\activate.bat
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 5001
echo.

pause

