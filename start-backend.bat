@echo off
REM The Bharat Collections - Backend Startup Script
REM This script installs dependencies and starts the Flask server

echo.
echo ========================================
echo  The Bharat Collections Backend Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python found: 
python --version
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Start Flask server
echo ========================================
echo Starting Flask Backend Server...
echo ========================================
echo.
echo Server will run on: http://localhost:5000
echo.
echo Frontend URL: file:///C:/Users/adity/Desktop/THE%%20BHARAT%%20COLLECTIONS/index.html
echo API Docs: http://localhost:5000/api/docs
echo Health Check: http://localhost:5000/api/health
echo.
echo Press Ctrl+C to stop the server
echo.

python backend/app.py
pause
