#!/bin/bash

echo "========================================"
echo " Sip & Puff Controller GUI"
echo "========================================"
echo ""

# Prüfe ob Python3 installiert ist
if ! command -v python3 &> /dev/null; then
    echo "FEHLER: Python3 ist nicht installiert!"
    echo "Bitte installiere Python3"
    exit 1
fi

echo "[1/2] Installiere Abhängigkeiten..."
pip3 install -r requirements.txt > /dev/null 2>&1

echo "[2/2] Starte GUI..."
echo ""
python3 sippuff_gui.py

echo ""
echo "Drücke Enter zum Beenden..."
read
