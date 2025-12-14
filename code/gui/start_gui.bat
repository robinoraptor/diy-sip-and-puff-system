@echo off
echo ========================================
echo  Sip ^& Puff Controller GUI
echo ========================================
echo.

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert!
    echo Bitte installiere Python von https://www.python.org/
    pause
    exit /b 1
)

echo [1/2] Installiere Abhängigkeiten...
pip install -r requirements.txt >nul 2>&1

echo [2/2] Starte GUI...
echo.
python sippuff_gui.py

pause
