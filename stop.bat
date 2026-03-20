@echo off
echo Stopping AI Assistant processes...

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8600') do taskkill /f /pid %%a
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3600') do taskkill /f /pid %%a

echo Processes stopped.
pause
