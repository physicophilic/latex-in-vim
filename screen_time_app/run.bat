@echo off
REM Launcher script for Take Time Back screen time tracker (Windows)

echo Starting Take Time Back - Screen Time Tracker...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Install dependencies if needed
python -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the application
python main.py
pause
