@echo off
:: Ensure we are in the script's directory (fixes Administrator mode path issue)
cd /d "%~dp0"
echo.

echo  =========================================
echo    MyNetShield Production Server Launcher
echo  =========================================
echo.

:: Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running with Administrator privileges.
) else (
    echo [ERROR] PLEASE RESTART THIS SCRIPT AS ADMINISTRATOR!
    echo.
    echo Right-click this file and select "Run as administrator".
    pause
    exit
)

echo [1/2] Activating environment...
:: Assuming the venv is in the same directory
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

echo [2/2] Starting Production Server (Waitress)...
echo.
echo Dashboard will be available at: http://localhost:5173

echo.
echo Press Ctrl+C to stop the server.
echo.

python production_run.py

pause
