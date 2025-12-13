# Sip & Puff Mouse Controller

> Ein adaptives Eingabesystem für Menschen mit eingeschränkter Fingermotorik

![System Overview](docs/images/system_overview.jpg)
*Platzhalter: Gesamtansicht des aufgebauten Systems*

---

## 📖 Über das Projekt

Dieses Projekt entstand im Rahmen eines **Human Factors (HF) Projekts** an der **Hochschule Furtwangen** und verfolgt die Fragestellung:

> **"Wie können durch eine Assistenzlösung zusätzliche, intuitiv nutzbare Freiheitsgrade geschaffen werden, die Menschen mit eingeschränkter Fingermotorik das selbstständige Ausführen der Maussteuerung ermöglichen?"**

### Definition Freiheitsgrad

*"Ein Freiheitsgrad ist eine (kontinuierliche) Dimension, die vom Eingabegerät erfasst und vom Benutzer unabhängig gesteuert werden kann."*  
— Seinfeld et al. (2020): User Representations in Human-Computer Interaction

---

## 🎯 Projektziele

Das System wurde entwickelt mit Fokus auf:

1. **Ausdrucksstarke Schnittstelle**  
   Maximaler digitaler Output bei minimalem physischem Aufwand

2. **Nutzerzentrierung**  
   Übertragbarkeit auf alle Menschen mit ähnlichen Einschränkungen

3. **Alltagsverbesserung**  
   Mehr Selbstständigkeit bei der PC-Bedienung für Menschen mit Einschränkungen

4. **Intuitive Bedienung**  
   Natürliche Interaktion durch Sip & Puff (Saug- und Blastechnik)

### Inspiration

Das Projekt orientiert sich an professionellen Assistenzsystemen wie dem **Quadstick** und ähnlichen kommerziellen Produkten, bietet aber eine **Open-Source-Alternative** zum Selbstbau.

---

## 🔄 Entwicklungsprozess & Prototypen

Die Entwicklung erfolgte iterativ in mehreren Prototyp-Versionen:

### Version 1.0 - Proof of Concept
![Prototyp v1.0](docs/images/prototype_v1.jpg)
*Platzhalter: Erster Prototyp auf Breadboard*

**Features:**
- Basis-Funktionalität (Sip & Puff für Klicks)
- Breadboard-Aufbau
- Einfacher Arduino-Code

**Erkenntnisse:**
- Drucksensor-Kalibrierung essentiell
- Schwellwerte müssen anpassbar sein

### Version 2.0 - Joystick Integration
![Prototyp v2.0](docs/images/prototype_v2.jpg)
*Platzhalter: Zweiter Prototyp mit Joystick*

**Features:**
- Joystick für 2D-Mausbewegung
- Verbesserte Kalibrierung
- Erste GUI-Tests

**Erkenntnisse:**
- Deadzone notwendig für präzise Steuerung
- Geschwindigkeitsanpassung wichtig

### Version 3.0 - GUI-gesteuert
![Prototyp v3.0](docs/images/prototype_v3.jpg)
*Platzhalter: Finaler Prototyp mit GUI*

**Features:**
- Vollständige GUI-Integration
- Echtzeit-Parameteranpassung
- Persistente Einstellungen
- Moderne CustomTkinter-UI

**Erkenntnisse:**
- Live-Anpassung drastisch verbessert Nutzbarkeit
- Individuelle Profile essentiell

### Version 4.0 - Produktionsreif (aktuell)
![Prototyp v4.0](docs/images/prototype_v4.jpg)
*Platzhalter: Aktueller Stand mit optimierter Hardware*

**Features:**
- Optimierte Hardware-Anordnung
- Stabilere Verkabelung
- Verbessertes Gehäuse-Konzept
- Umfassende Dokumentation

**Nächste Schritte:**
- 3D-gedrucktes Gehäuse
- Wireless-Option (Bluetooth)
- Profile-System

---

## ✨ Features

### Hardware
- ✅ **MPXV7002DP Drucksensor** für bidirektionale Druckmessung (Saugen/Blasen)
- ✅ **Analoger Joystick** für präzise 2D-Mausbewegung
- ✅ **Arduino Pro Micro** als USB-HID-Gerät (native Mausfunktion)
- ✅ **Modularer Aufbau** für einfache Anpassungen

### Software
- ✅ **Moderne GUI** mit CustomTkinter für Echtzeit-Konfiguration
- ✅ **Live-Parameteranpassung** ohne Arduino-Neustart
- ✅ **Persistente Einstellungen** (JSON-basiert)
- ✅ **Drei Klick-Modi**: Linksklick, Doppelklick, Rechtsklick
- ✅ **Adaptive Schwellwerte** (-400 bis +400)
- ✅ **Joystick aktivierbar/deaktivierbar**

![GUI Screenshot](docs/images/gui_screenshot.png)
*Platzhalter: Screenshot der Konfigurations-GUI*

---

## 🛠️ Hardware-Komponenten

| Komponente | Typ | Funktion | Ungefähre Kosten | Link |
|------------|-----|----------|------------------|------|
| Arduino Pro Micro | ATmega32U4 | Mikrocontroller mit nativer USB-HID-Unterstützung | 8,59 € | https://www.amazon.de/EntwicklungBoards-Binghe-Mikrocontroller-Entwicklungsboard-Selbst-USB-Updater/dp/B0D69JLJ97/ref=sr_1_1_pp?crid=3FBKSPF7ND7OH&dib=eyJ2IjoiMSJ9.m9zoZdlvH_p8LU9pMV4IJOJ5KPBbrCMNkZKKCmBEfpgtMUrJUq3ggsoOKdUmjuCV-_4V8o2hM9JqLgg1LsCxJrqLudyg19aJPjiBQp9CXK9PtmK0OKS_Sbb1JXT7yrYkMQuxoDDsUkRYc62Lx7b0D6K2BUTU9blUNgKt7_nZxJ8fxKc4lztovX7qqiIkRWlJ1ZIY5JQ4TXoqx5tw3sI0ED9u32NgMS9CbSdakyHV2js.hyoTs0gNzm_DUlIygOJR_kxBFjo83G-4MAdEWQnrUYg&dib_tag=se&keywords=arduino+pro+micro&qid=1765627500&sprefix=arduino+pro+%2Caps%2C114&sr=8-1
| MPXV7002DP | Drucksensor | Bidirektionaler Differenzdrucksensor (±2 kPa) | ~15-20 € |
| Analoger Joystick | 2-Achsen | XY-Achsen für Mausbewegung | ~2-5 € |
| Kippschalter | SPST | Optional: Joystick-Aktivierung | ~1 € |
| Taster | Momentary | Reset-Button | ~0,50 € |
| Schlauch + Mundstück | Medizinisch | Für Sip & Puff Eingabe | ~5-10 € |
| Diverse | Kabel, Breadboard, Gehäuse | Verkabelung und Montage | ~5-10 € |
| **Gesamt** | | | **~35-60 €** |

![Hardware Setup](docs/images/hardware_setup.jpg)
*Platzhalter: Foto des Hardwareaufbaus*

---

## 🔌 Schaltplan

### Pin-Belegung Arduino Pro Micro

```
MPXV7002DP Drucksensor:
├─ VCC  → 5V (Arduino)
├─ GND  → GND (Arduino)
└─ OUT  → A0 (Analog)

Joystick:
├─ VCC  → RAW (5V Arduino)
├─ GND  → GND (Arduino, optional über Kippschalter)
├─ VRx  → A2 (Analog)
└─ VRy  → A1 (Analog)

Reset-Button:
├─ Pin 1 → GND
└─ Pin 2 → RST
```

![Wiring Diagram](docs/images/wiring_diagram.png)
*Platzhalter: Schaltplan/Fritzing-Diagramm*

---

## 📦 Installation

### Voraussetzungen

**Hardware:**
- Arduino Pro Micro (oder kompatibel)
- USB-Kabel (Micro-USB)
- Aufgebaute Schaltung (siehe Schaltplan)

**Software:**
- [PlatformIO](https://platformio.org/) oder Arduino IDE
- Python 3.7+ (für GUI)
- Git (optional)

### 1. Repository klonen

```bash
git clone https://github.com/DEIN-USERNAME/sip-puff-controller.git
cd sip-puff-controller
```

### 2. Arduino-Code flashen

#### Mit PlatformIO (empfohlen):

```bash
cd arduino/
pio run --target upload
```

#### Mit Arduino IDE:
1. `arduino/src/main.cpp` öffnen
2. Board auswählen: **Tools → Board → SparkFun Pro Micro (5V, 16 MHz)**
3. Port auswählen: **Tools → Port → [Dein Port]**
4. Hochladen: **Sketch → Upload**

### 3. GUI installieren

#### Automatisch (empfohlen):

**Linux/macOS:**
```bash
cd gui/
./start_gui.sh
```

**Windows:**
```bash
cd gui/
start_gui.bat
```

#### Manuell:

```bash
cd gui/
pip install -r requirements.txt
python sippuff_gui.py
```

---

## 🚀 Verwendung

### Ersteinrichtung

1. **Arduino anschließen**
   - System kalibriert automatisch beim Start
   - ⚠️ **Wichtig:** NICHT in den Schlauch pusten/saugen während der Kalibrierung!

2. **GUI starten**
   ```bash
   python sippuff_gui.py
   ```

3. **Verbinden**
   - Port auswählen (z.B. COM3 oder /dev/ttyACM0)
   - "Verbinden" klicken

4. **Einstellungen anpassen**
   - Mit Slidern experimentieren
   - Echtzeit-Feedback im Log

### Steuerung

![Control Scheme](docs/images/control_scheme.png)
*Platzhalter: Grafische Darstellung der Steuerung*

#### Standard-Belegung:

| Aktion | Eingabe | Beschreibung |
|--------|---------|--------------|
| **Linksklick** | Sip (Saugen) < -10 | Leichtes Ansaugen |
| **Doppelklick** | Sip (Saugen) < -15 | Kräftiges Ansaugen |
| **Rechtsklick** | Puff (Blasen) > 10 | Leichtes Blasen |
| **Mausbewegung** | Joystick | 2D-Bewegung in alle Richtungen |

#### Anpassbare Parameter:

- **Klick-Schwellwerte:** -400 bis +400
- **Joystick-Geschwindigkeit:** 5-50
- **Deadzone:** 0-100
- **Update-Rate:** 10-100ms
- **Debounce:** 100-1000ms

### Einstellungen speichern

- **"Speichern"** → Wird in `sippuff_config.json` gespeichert
- **"Standard"** → Lädt Standardwerte aus `sippuff_defaults.json`
- Beim nächsten Start werden gespeicherte Einstellungen automatisch geladen

---

## 🔧 Konfiguration

### Schwellwerte anpassen

Die Empfindlichkeit kann individuell angepasst werden:

```
Für Nutzer mit schwächerer Atemkontrolle:
├─ Linksklick: -5
├─ Doppelklick: -8
└─ Rechtsklick: 5

Für Nutzer mit stärkerer Atemkontrolle:
├─ Linksklick: -30
├─ Doppelklick: -50
└─ Rechtsklick: 30
```

### Standard-Werte ändern

Editiere `gui/sippuff_defaults.json`:

```json
{
  "click_left": -10,
  "click_double": -15,
  "click_right": 10,
  "wavelength": 15,
  "period": 35,
  "deadzone": 25,
  "debounce": 500,
  "joystick_enabled": true
}
```

---

## 📁 Projektstruktur

```
sip-puff-controller/
├── arduino/                    # Arduino-Firmware
│   ├── src/
│   │   └── main.cpp           # Hauptcode mit Serial-Protokoll
│   └── platformio.ini         # PlatformIO-Konfiguration
│
├── gui/                        # Python-GUI
│   ├── sippuff_gui.py         # Haupt-Anwendung
│   ├── requirements.txt       # Python-Dependencies
│   ├── start_gui.sh           # Linux/macOS-Starter
│   ├── start_gui.bat          # Windows-Starter
│   ├── sippuff_config.json    # Nutzer-Einstellungen (wird erstellt)
│   ├── sippuff_defaults.json  # Standard-Werte (wird erstellt)
│   ├── UNICODE_SYMBOLE.md     # Icon-Referenz
│   └── UI_ANPASSUNGEN.md      # UI-Customization-Guide
│
├── docs/                       # Dokumentation
│   └── images/                 # Screenshots und Fotos
│       ├── system_overview.jpg
│       ├── hardware_setup.jpg
│       ├── gui_screenshot.png
│       ├── wiring_diagram.png
│       └── control_scheme.png
│
├── LICENSE                     # MIT Lizenz
└── README.md                   # Diese Datei
```

---

## 🔬 Technische Details

### Arduino-Firmware

- **Sprache:** C++ (Arduino Framework)
- **Bibliotheken:** `Mouse.h` (native USB-HID)
- **Sampling-Rate:** 100 Hz (10ms Loop)
- **Kalibrierung:** Automatisch beim Start (50 Samples, 1 Sekunde)
- **Serial-Protokoll:** 115200 Baud für GUI-Kommunikation

### GUI-Anwendung

- **Framework:** CustomTkinter (moderne UI)
- **Kommunikation:** PySerial
- **Architektur:** Event-driven mit Threading
- **Plattformen:** Windows, macOS, Linux

### Serial-Protokoll (Auszug)

```
Arduino → GUI:
├─ ACTION:LEFT_CLICK          # Klick ausgeführt
├─ SETTINGS:START             # Einstellungen folgen
├─ CLICK_LEFT:-10             # Parameter-Wert
└─ SETTINGS:END               # Ende der Übertragung

GUI → Arduino:
├─ SET:CLICK_LEFT:-10         # Parameter setzen
├─ GET:SETTINGS               # Einstellungen abrufen
└─ RECALIBRATE                # Neu kalibrieren
```

---

## 🐛 Troubleshooting

### Arduino wird nicht erkannt

**Problem:** Port erscheint nicht in der GUI

**Lösungen:**
- USB-Kabel prüfen (Datenkabel, kein reines Ladekabel)
- Treiber installieren (CH340 oder ATmega32U4)
- Anderen USB-Port verwenden
- "🔄" Button in der GUI klicken

### Klicks werden nicht erkannt

**Problem:** Saugen/Blasen löst keine Aktion aus

**Lösungen:**
1. Rekalibrieren (ohne Pusten/Saugen!)
2. Schwellwerte senken (z.B. -5 / 5)
3. Sensor-Anschluss prüfen
4. Im Serial Monitor Rohwerte beobachten

### Maus bewegt sich nicht

**Problem:** Joystick hat keine Wirkung

**Lösungen:**
- Joystick-Checkbox aktiviert?
- Verkabelung prüfen (besonders GND)
- Deadzone verkleinern (< 25)
- Joystick-Werte im Serial Monitor prüfen

### GUI startet nicht

**Problem:** Python-Fehler beim Start

**Lösungen:**
```bash
# Dependencies neu installieren
pip install --upgrade -r requirements.txt

# Python-Version prüfen
python --version  # Sollte >= 3.7 sein

# Manuell starten
python sippuff_gui.py
```

---

## 🔄 Weiterentwicklung

### Mögliche Erweiterungen

- [ ] **Wireless-Modus** via Bluetooth (ESP32)
- [ ] **Zusätzliche Buttons** für Shortcuts (Strg, Alt, etc.)
- [ ] **Profile-System** für verschiedene Anwendungen
- [ ] **Makro-Aufzeichnung** für wiederkehrende Aktionen
- [ ] **Barrierefreie Tastatur-Eingabe**
- [ ] **Integration mit Eye-Tracking**
- [ ] **3D-druckbares Gehäuse** (STL-Dateien)

### Beiträge willkommen! 🤝

Issues und Pull Requests sind herzlich willkommen. Bei größeren Änderungen bitte zuerst ein Issue öffnen.

---

## 📚 Wissenschaftlicher Hintergrund

### Literatur

**Seinfeld, S., Feuchtner, T., Maselli, A. & Müller, J. (2020).**  
*User Representations in Human-Computer Interaction.*  
Human-Computer Interaction, 36(5–6), 400–438.  
https://doi.org/10.1080/07370024.2020.1724790

### Verwandte Projekte

- **Quadstick** - Kommerzielles Sip & Puff System
- **Xbox Adaptive Controller** - Microsoft's Adaptive Gaming Controller
- **Camera Mouse** - Eye-Tracking basierte Maussteuerung

---

## ⚠️ Sicherheitshinweise

### Wichtig für die Nutzung:

1. **Hygiene**
   - Mundstück täglich reinigen/desinfizieren
   - Schlauch regelmäßig austauschen
   - Bei mehreren Nutzern: individuelle Mundstücke verwenden

2. **Gesundheit**
   - Bei Schwindel/Unwohlsein sofort pausieren
   - Nicht zu stark/häufig pusten (Hyperventilation vermeiden)
   - Regelmäßige Pausen einlegen

3. **Technisch**
   - System nicht unbeaufsichtigt mit anderen Nutzern betreiben
   - Bei Fehlfunktion sofort vom Computer trennen
   - Keine Modifikationen an medizinischen Komponenten

4. **Medizinisch**
   - Dieses System ist **kein medizinisches Produkt**
   - Keine CE-Kennzeichnung für Medizinprodukte
   - Bei medizinischer Nutzung: Rücksprache mit Fachpersonal

---

## 🎓 Hochschule Furtwangen

Entwickelt im Rahmen eines Human Factors Projekts an der **Hochschule Furtwangen University (HFU)**.

**Fakultät:** Engineering Technology  
**Studiengang:** Human Factors 
**Semester:** 2. Semester  

---

## 🙏 Danksagung

Besonderer Dank gilt:

- Allen Testern und Nutzern des Systems für wertvolles Feedback
- Der Hochschule Furtwangen für die Unterstützung
- Der Open-Source-Community für Tools und Bibliotheken

---

## 📧 Kontakt & Support

**Fragen zum Projekt?**
- GitHub Issues: [Issues öffnen](https://github.com/DEIN-USERNAME/sip-puff-controller/issues)
- Diskussionen: [Discussions](https://github.com/DEIN-USERNAME/sip-puff-controller/discussions)

---

**⭐ Wenn dir dieses Projekt geholfen hat, gib ihm gerne einen Stern auf GitHub!**

---

*Entwickelt mit ❤️ für mehr Barrierefreiheit und Selbstständigkeit*
