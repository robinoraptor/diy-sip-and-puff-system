#!/bin/bash
# Build-Skript für Mac .app / Linux
# Erstellt eine standalone Anwendung

echo "========================================"
echo "  Sip & Puff GUI - Mac/Linux Build"
echo "========================================"
echo ""

# Prüfe ob PyInstaller installiert ist
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller nicht gefunden, installiere..."
    pip3 install pyinstaller
fi

echo ""
echo "Erstelle Anwendung..."
echo ""

# Erstelle .app (Mac) oder Binary (Linux)
pyinstaller --onefile \
    --windowed \
    --name "SipPuffController" \
    --add-data "theme_red.json:." \
    --hidden-import "customtkinter" \
    --hidden-import "serial" \
    --hidden-import "serial.tools.list_ports" \
    sippuff_gui.py

echo ""
echo "========================================"
echo "  Build abgeschlossen!"
echo "========================================"
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Die .app findest du in: dist/SipPuffController.app"
else
    echo "Die Binary findest du in: dist/SipPuffController"
fi

echo ""