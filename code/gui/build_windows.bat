@echo off
REM Build-Skript für Windows .exe
REM Erstellt eine standalone .exe Datei

echo ========================================
echo  Sip & Puff GUI - Windows Build
echo ========================================
echo.

REM Prüfe ob PyInstaller installiert ist
python -c "import PyInstaller" 2>NUL
if errorlevel 1 (
    echo PyInstaller nicht gefunden, installiere...
    pip install pyinstaller
)

echo.
echo Erstelle Windows .exe...
echo.

REM Erstelle .exe mit allen Dependencies
pyinstaller --onefile ^
    --windowed ^
    --name "SipPuffController" ^
    --icon=NONE ^
    --add-data "theme_red.json;." ^
    --hidden-import "customtkinter" ^
    --hidden-import "serial" ^
    --hidden-import "serial.tools.list_ports" ^
    sippuff_gui.py

echo.
echo ========================================
echo  Build abgeschlossen!
echo ========================================
echo.
echo Die .exe findest du in: dist\SipPuffController.exe
echo.
pause