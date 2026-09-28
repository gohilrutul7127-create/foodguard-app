@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

if not exist "logs" mkdir logs

start "FoodGuard Backend" powershell -NoExit -ExecutionPolicy Bypass -File "%~dp0\start-foodguard-backend.ps1"
start "FoodGuard Frontend" powershell -NoExit -ExecutionPolicy Bypass -File "%~dp0\start-foodguard-frontend.ps1"

echo FoodGuard starting...
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000
echo.
if exist "%~dp0\ngrok.exe" (
    echo Starting public tunnel...
    start "FoodGuard Tunnel" powershell -NoExit -ExecutionPolicy Bypass -Command "cd '%~dp0'; .\ngrok.exe http 5173"
) else (
    echo ngrok.exe not found yet. Download it and place it in the project root to enable the public link.
)
pause
