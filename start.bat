@echo off
setlocal
title AI Document Assistant Pro - Starter
set PYTHONPATH=%CD%
echo [INFO] Starting AI Document Assistant...
echo [INFO] Environment: %CD%

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not found. Please install Python and add it to your PATH.
    pause
    exit /b 1
)

:: Run the app
python run_app.py

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Application failed to start or crashed.
    pause
)
