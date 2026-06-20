@echo off
echo ==============================================
echo   MyNetShield Backend PyInstaller Builder
echo ==============================================
echo.
echo [1/3] Activating Virtual Environment...
call venv\Scripts\activate.bat

echo [2/3] Building Frontend via Vite...
cd app\dashboard\frontend
call npm run build
cd ..\..\..

echo [3/3] Compiling Backend with PyInstaller...
if not exist "app\ml\models" mkdir "app\ml\models"
pyinstaller ^
  --name "backend" ^
  --onedir ^
  --clean ^
  --noconfirm ^
  --add-data "app/dashboard/frontend/dist;app/dashboard/frontend/dist" ^
  --add-data "app/dashboard/fonts;app/dashboard/fonts" ^
  --add-data "app/ml/models;app/ml/models" ^
  --hidden-import "waitress" ^
  --hidden-import "flask_cors" ^
  --hidden-import "scapy.layers.l2" ^
  --hidden-import "scapy.layers.inet" ^
  --hidden-import "xhtml2pdf" ^
  --hidden-import "reportlab" ^
  production_run.py

echo.
echo ==============================================
echo   Backend Compilation Complete!
echo   Executable is in 'dist/backend/backend.exe'
echo ==============================================
pause
