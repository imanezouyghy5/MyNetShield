@echo off
echo ==============================================
echo Installing MyNetShield Dependencies...
echo ==============================================

echo 1. Setting up Python Virtual Environment...
python -m venv venv
call venv\Scripts\activate.bat

echo 2. Installing Python Requirements...
pip install -r requirements.txt

echo 3. Installing Node.js Frontend Dependencies...
cd app\dashboard\frontend
call npm install
cd ..\..\..

echo.
echo ==============================================
echo Installation Complete!
echo You can now run the app using: start_netshield.bat
echo ==============================================
pause
