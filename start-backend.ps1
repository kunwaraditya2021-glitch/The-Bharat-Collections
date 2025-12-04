# The Bharat Collections - Backend Startup Script (PowerShell)
# This script installs dependencies and starts the Flask server

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  The Bharat Collections Backend Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Start Flask server
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Flask Backend Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Server will run on: http://localhost:5000" -ForegroundColor Green
Write-Host "Frontend URL: file:///C:/Users/adity/Desktop/THE%20BHARAT%20COLLECTIONS/index.html" -ForegroundColor Green
Write-Host "API Docs: http://localhost:5000/api/docs" -ForegroundColor Green
Write-Host "Health Check: http://localhost:5000/api/health" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python backend/app.py
