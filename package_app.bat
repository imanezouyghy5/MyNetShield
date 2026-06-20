@echo off
:: Ensure we are in the script's directory (fixes Administrator mode path issue)
cd /d "%~dp0"
echo ==============================================
echo   MyNetShield PRO - Desktop App Packager
echo ==============================================
echo.
echo Cleaning old builds...
if exist "app\dashboard\frontend\release" rmdir /s /q "app\dashboard\frontend\release"
if exist "app\dashboard\frontend\dist_backend" rmdir /s /q "app\dashboard\frontend\dist_backend"

echo Copying backend to local build folder...
mkdir "app\dashboard\frontend\dist_backend"
xcopy /e /i /y "dist\backend" "app\dashboard\frontend\dist_backend"

echo Packaging React Frontend and Python Backend into Setup Installer...
cd app\dashboard\frontend
call npm run electron:build

echo.
echo ==============================================
echo   Packaging Complete!
echo   Your installer is located at:
echo   app\dashboard\frontend\release\MyNetShield Setup X.Y.Z.exe
echo ==============================================
pause
