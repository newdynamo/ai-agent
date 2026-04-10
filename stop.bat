@echo off
setlocal
title Stopping AI Assistant...
echo [INFO] Stopping AI Assistant processes...

:: Killing Backend (Port 8600)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /r "LISTENING.*:8600"') do (
    echo [INFO] Terminating backend (PID: %%a)...
    taskkill /f /t /pid %%a >nul 2>&1
)

:: Killing Frontend (Port 3600)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /r "LISTENING.*:3600"') do (
    echo [INFO] Terminating frontend (PID: %%a)...
    taskkill /f /t /pid %%a >nul 2>&1
)

echo [INFO] Processes stopped successfully.
pause
