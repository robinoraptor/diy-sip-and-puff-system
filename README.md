# Sip & Puff Mouse Controller

> Ein adaptives Eingabesystem für Menschen mit eingeschränkter Fingermotorik

![System Overview](docs/images/protoype_v1_a.jpeg)

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
![Prototyp v1.0 a](docs/images/protoype_v1_a.jpeg)
![Prototyp v1.0 b](docs/images/protoype_v1_b.jpeg)

**Features:**
- Basis-Funktionalität (Sip & Puff für Klicks)
- Joystick für 2D-Mausbewegung
- Lötverbindung der Komponenten
- Einfacher Arduino-Code

**Erkenntnisse:**
- Drucksensor-Kalibrierung essentiell
- Schwellwerte müssen anpassbar sein
- Deadzone notwendig für präzise Steuerung
- Geschwindigkeitsanpassung wichtig

### Version 2.0 - GUI-gesteuert
![Prototyp v3.0](docs/images/gui_v1.png)

**Features:**
- Vollständige GUI-Integration
- Echtzeit-Parameteranpassung
- Persistente Einstellungen
- Moderne CustomTkinter-UI

**Erkenntnisse:**
- Live-Anpassung drastisch verbessert Nutzbarkeit
- Individuelle Profile essentiell

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

![GUI Screenshot](docs/images/gui_v1.png)

---

## 🛠️ Hardware-Komponenten

| Komponente | Typ | Funktion | Ungefähre Kosten | Link |
|------------|-----|----------|------------------|------|
| Arduino Pro Micro | ATmega32U4 | Mikrocontroller mit nativer USB-HID-Unterstützung | ~8 € | https://www.amazon.de/EntwicklungBoards-Binghe-Mikrocontroller-Entwicklungsboard-Selbst-USB-Updater/dp/B0D69JLJ97/ref=sr_1_1_pp?crid=3FBKSPF7ND7OH&dib=eyJ2IjoiMSJ9.m9zoZdlvH_p8LU9pMV4IJOJ5KPBbrCMNkZKKCmBEfpgtMUrJUq3ggsoOKdUmjuCV-_4V8o2hM9JqLgg1LsCxJrqLudyg19aJPjiBQp9CXK9PtmK0OKS_Sbb1JXT7yrYkMQuxoDDsUkRYc62Lx7b0D6K2BUTU9blUNgKt7_nZxJ8fxKc4lztovX7qqiIkRWlJ1ZIY5JQ4TXoqx5tw3sI0ED9u32NgMS9CbSdakyHV2js.hyoTs0gNzm_DUlIygOJR_kxBFjo83G-4MAdEWQnrUYg&dib_tag=se&keywords=arduino+pro+micro&qid=1765627500&sprefix=arduino+pro+%2Caps%2C114&sr=8-1 |
| MPXV7002DP | Drucksensor | Bidirektionaler Differenzdrucksensor (±2 kPa) | ~24 € | https://www.amazon.de/dp/B08D6JDJ4D?ref=ppx_yo2ov_dt_b_fed_asin_title |
| Analoger Joystick | 2-Achsen | XY-Achsen für Mausbewegung | ~1 € | https://www.roboter-bausatz.de/p/joystick-modul-2-achsen |
| Schlauch 2.5mm ID x 4mm OD x 1m | Silikon (Lebensmittelecht) | Für Sip & Puff Eingabe | ~4 € | https://www.amazon.de/dp/B0BZXR88VD?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1 |
| Schlauch 3mm ID x 6mm OD x 1.5m | Silikon (Lebensmittelecht) | Für Sip & Puff Eingabe | ~5 € | https://www.amazon.de/dp/B0CXPW74GZ?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1 |
| PTFE Filter | Hydrophob | Hygiene & Schutz gegen Flüssigkeit | ~14 € | https://www.amazon.de/dp/B07KWW7ZXF?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1 |
| Luer Lock Adapter | Weiblich | Verbindung von Filter & Schlauch | ~7 € | https://www.amazon.de/dp/B0BMFJSJP1?ref=ppx_yo2ov_dt_b_fed_asin_title |
| Luer Lock Adapter | Männlich | Verbindung von Filter & Schlauch | ~8 € | https://www.amazon.de/dp/B0B8CJVX3S?ref=ppx_yo2ov_dt_b_fed_asin_title |
| Diverse | Kabel, LEDs, Gehäuse | Verkabelung und Montage | ~5-10 € |
| **Gesamt** | | | **~35-60 €** |

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
git clone https://github.com/robinoraptor/sip-puff-controller.git
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
