/*
 * Sip and Puff Mouse Controller with GUI Configuration
 * Arduino Pro Micro mit MPXV7002DP Drucksensor + Joystick
 *
 * Steuerung über Serial-Kommandos für Echtzeit-Parameteränderung
 */

#include <Mouse.h>

// Pin-Definitionen
const int PRESSURE_PIN = A0; // MPXV7002DP Drucksensor
const int JOY_X_PIN = A2;    // Joystick X-Achse
const int JOY_Y_PIN = A1;    // Joystick Y-Achse

// Kalibrierung
int pressureBaseline = 0; // Nullpunkt bei Umgebungsdruck
const int SAMPLES = 50;   // Anzahl Samples für Kalibrierung

// Klick-Schwellwerte (über Serial änderbar)
int clickLeft = 10;   // Einfacher Linksklick (Pusten)
int clickDouble = 15; // Doppelter Linksklick (starkes Pusten)
int clickRight = -10; // Rechtsklick (Saugen)

// Scroll-Schwellwerte (über Serial änderbar)
int scrollUp = -5;         // Scroll nach oben (leichtes Saugen)
int scrollDown = 5;        // Scroll nach unten (leichtes Pusten)
int scrollSpeed = 1;       // Scroll-Geschwindigkeit (1-5)
bool scrollEnabled = true; // Scroll aktivierbar/deaktivierbar

// Debouncing für Klicks (über Serial änderbar)
unsigned long lastClickTime = 0;
unsigned long clickDebounce = 500; // 500ms zwischen Klicks

// Joystick-Einstellungen (über Serial änderbar)
const int JOY_CENTER = 512; // Mittelposition des Joysticks
int joyDeadzone = 25;       // Deadzone um Mittelposition
int wavelength = 15;        // Geschwindigkeit in Pixel pro Iteration
int period = 35;            // Update-Intervall in MS
unsigned long cursorFrequencyTimer = 0;

// Joystick-Aktivierung (über Serial änderbar)
bool joystickEnabled = true;

// Status-LED
const int LED_PIN = LED_BUILTIN_TX;

// Serial-Kommando-Buffer
String serialBuffer = "";
bool commandReady = false;

// Drucktest-Modus
bool pressureTestMode = false; // Wenn true, sende kontinuierlich Druckwerte

// Function Prototypes
void calibratePressureSensor();
void handleClicks(int pressureDiff);
void handleScrolling(int pressureDiff);
void handleMouseMovement();
void blinkLED(int times);
void processSerialCommand(String cmd);
void sendCurrentSettings();

void setup()
{
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  Serial.begin(115200);
  delay(1000);

  Serial.println(F("================================="));
  Serial.println(F("  Sip & Puff Mouse Controller"));
  Serial.println(F("================================="));
  Serial.println();

  // Kalibrierung des Drucksensors
  calibratePressureSensor();

  // Maus initialisieren
  Mouse.begin();

  // Timer initialisieren
  cursorFrequencyTimer = millis() + period;

  Serial.println(F("\n>>> Controller aktiv <<<"));
  Serial.println(F("Bereit für GUI-Verbindung\n"));

  // Sende aktuelle Einstellungen
  sendCurrentSettings();

  digitalWrite(LED_PIN, LOW);
  delay(500);
}

void loop()
{
  // Serial-Kommandos verarbeiten
  while (Serial.available() > 0)
  {
    char c = Serial.read();
    if (c == '\n')
    {
      commandReady = true;
    }
    else
    {
      serialBuffer += c;
    }
  }

  if (commandReady)
  {
    processSerialCommand(serialBuffer);
    serialBuffer = "";
    commandReady = false;
  }

  // Drucksensor auslesen
  int pressureRaw = analogRead(PRESSURE_PIN);
  int pressureDiff = pressureRaw - pressureBaseline;

  // Drucktest-Modus: Sende kontinuierlich Werte
  if (pressureTestMode)
  {
    // Sende den Druck-Wert
    Serial.println(pressureDiff);
    delay(200); // 5Hz Update-Rate für Stabilität
  }
  else
  {
    // Mausklicks über Sip & Puff
    handleClicks(pressureDiff);

    // Scrolling über leichtes Sip & Puff (nur wenn aktiviert)
    if (scrollEnabled)
    {
      handleScrolling(pressureDiff);
    }

    // Mausbewegung über Joystick (wenn aktiviert)
    if (joystickEnabled && millis() >= cursorFrequencyTimer)
    {
      handleMouseMovement();
      cursorFrequencyTimer = millis() + period;
    }

    delay(10);
  }
}

void calibratePressureSensor()
{
  Serial.println(F("Kalibriere Drucksensor..."));
  Serial.println(F("Bitte NICHT in Schlauch pusten/saugen!"));

  long sum = 0;

  for (int i = 0; i < SAMPLES; i++)
  {
    sum += analogRead(PRESSURE_PIN);
    if (i % 10 == 0)
    {
      Serial.print(F("."));
    }
    delay(20);
  }

  pressureBaseline = sum / SAMPLES;

  Serial.println();
  Serial.print(F("Kalibrierung abgeschlossen! Nullpunkt: "));
  Serial.println(pressureBaseline);
}

void handleClicks(int pressureDiff)
{
  unsigned long currentTime = millis();

  if (currentTime - lastClickTime < clickDebounce)
  {
    return;
  }

  // Doppelklick (starkes Pusten)
  if (pressureDiff > clickDouble)
  {
    Serial.println(F("ACTION:DOUBLE_CLICK"));
    Mouse.click(MOUSE_LEFT);
    delay(50);
    Mouse.click(MOUSE_LEFT);
    lastClickTime = currentTime;
    blinkLED(2);
  }

  // Einfacher Linksklick (Pusten)
  else if (pressureDiff > clickLeft)
  {
    Serial.println(F("ACTION:LEFT_CLICK"));
    Mouse.click(MOUSE_LEFT);
    lastClickTime = currentTime;
    blinkLED(1);
  }

  // Rechtsklick (Saugen)
  else if (pressureDiff < clickRight)
  {
    Serial.println(F("ACTION:RIGHT_CLICK"));
    Mouse.click(MOUSE_RIGHT);
    lastClickTime = currentTime;
    blinkLED(1);
  }
}

void handleScrolling(int pressureDiff)
{
  // Scroll nur wenn kein Klick gerade passiert ist (Debounce-Zeit)
  unsigned long currentTime = millis();
  if (currentTime - lastClickTime < clickDebounce)
  {
    return;
  }

  // Scroll nach oben (leichtes Saugen)
  // Bereich: scrollUp bis clickRight (z.B. -5 bis -10)
  if (pressureDiff < scrollUp && pressureDiff >= clickRight)
  {
    Mouse.move(0, 0, scrollSpeed); // Positiv = scroll up
  }

  // Scroll nach unten (leichtes Pusten)
  // Bereich: scrollDown bis clickLeft (z.B. +5 bis +10)
  else if (pressureDiff > scrollDown && pressureDiff <= clickLeft)
  {
    Mouse.move(0, 0, -scrollSpeed); // Negativ = scroll down
  }
}

void handleMouseMovement()
{
  int joyX = analogRead(JOY_X_PIN);
  int joyY = analogRead(JOY_Y_PIN);

  int deltaX = joyX - JOY_CENTER;
  int deltaY = joyY - JOY_CENTER;

  // Deadzone anwenden
  if (abs(deltaX) < joyDeadzone)
  {
    deltaX = 0;
  }
  else
  {
    if (deltaX < 0)
    {
      deltaX += joyDeadzone;
    }
    else
    {
      deltaX -= joyDeadzone;
    }
  }

  if (abs(deltaY) < joyDeadzone)
  {
    deltaY = 0;
  }
  else
  {
    if (deltaY < 0)
    {
      deltaY += joyDeadzone;
    }
    else
    {
      deltaY -= joyDeadzone;
    }
  }

  // Geschwindigkeitsberechnung
  int moveX = deltaX / (1023 / (wavelength * 2));
  int moveY = deltaY / (1023 / (wavelength * 2));

  moveX = -moveX;
  moveY = -moveY;

  if (moveX != 0 || moveY != 0)
  {
    Mouse.move(moveX, moveY, 0);
  }
}

void blinkLED(int times)
{
  for (int i = 0; i < times; i++)
  {
    digitalWrite(LED_PIN, HIGH);
    delay(50);
    digitalWrite(LED_PIN, LOW);
    delay(50);
  }
}

void processSerialCommand(String cmd)
{
  cmd.trim();

  if (cmd.startsWith("SET:"))
  {
    String param = cmd.substring(4);
    int separatorIndex = param.indexOf(':');

    if (separatorIndex > 0)
    {
      String key = param.substring(0, separatorIndex);
      int value = param.substring(separatorIndex + 1).toInt();

      if (key == "CLICK_LEFT")
      {
        clickLeft = value;
        Serial.println(F("OK:CLICK_LEFT"));
      }
      else if (key == "CLICK_DOUBLE")
      {
        clickDouble = value;
        Serial.println(F("OK:CLICK_DOUBLE"));
      }
      else if (key == "CLICK_RIGHT")
      {
        clickRight = value;
        Serial.println(F("OK:CLICK_RIGHT"));
      }
      else if (key == "SCROLL_UP")
      {
        scrollUp = value;
        Serial.println(F("OK:SCROLL_UP"));
      }
      else if (key == "SCROLL_DOWN")
      {
        scrollDown = value;
        Serial.println(F("OK:SCROLL_DOWN"));
      }
      else if (key == "SCROLL_SPEED")
      {
        scrollSpeed = value;
        Serial.println(F("OK:SCROLL_SPEED"));
      }
      else if (key == "SCROLL")
      {
        scrollEnabled = (value == 1);
        Serial.print(F("OK:SCROLL:"));
        Serial.println(scrollEnabled ? "ON" : "OFF");
      }
      else if (key == "WAVELENGTH")
      {
        wavelength = value;
        Serial.println(F("OK:WAVELENGTH"));
      }
      else if (key == "PERIOD")
      {
        period = value;
        Serial.println(F("OK:PERIOD"));
      }
      else if (key == "DEADZONE")
      {
        joyDeadzone = value;
        Serial.println(F("OK:DEADZONE"));
      }
      else if (key == "DEBOUNCE")
      {
        clickDebounce = value;
        Serial.println(F("OK:DEBOUNCE"));
      }
      else if (key == "JOYSTICK")
      {
        joystickEnabled = (value == 1);
        Serial.print(F("OK:JOYSTICK:"));
        Serial.println(joystickEnabled ? "ON" : "OFF");
      }
    }
  }
  else if (cmd == "GET:SETTINGS")
  {
    sendCurrentSettings();
  }
  else if (cmd == "RECALIBRATE")
  {
    Serial.println(F("INFO:Starte Rekalibrierung..."));
    calibratePressureSensor();
    Serial.println(F("OK:RECALIBRATE"));
  }
  else if (cmd == "PRESSURE_TEST:START")
  {
    pressureTestMode = true;
    Serial.println(F("OK:PRESSURE_TEST:START"));
  }
  else if (cmd == "PRESSURE_TEST:STOP")
  {
    pressureTestMode = false;
    Serial.println(F("OK:PRESSURE_TEST:STOP"));
  }
}

void sendCurrentSettings()
{
  Serial.println(F("SETTINGS:START"));
  Serial.print(F("CLICK_LEFT:"));
  Serial.println(clickLeft);
  Serial.print(F("CLICK_DOUBLE:"));
  Serial.println(clickDouble);
  Serial.print(F("CLICK_RIGHT:"));
  Serial.println(clickRight);
  Serial.print(F("SCROLL_UP:"));
  Serial.println(scrollUp);
  Serial.print(F("SCROLL_DOWN:"));
  Serial.println(scrollDown);
  Serial.print(F("SCROLL_SPEED:"));
  Serial.println(scrollSpeed);
  Serial.print(F("SCROLL:"));
  Serial.println(scrollEnabled ? "1" : "0");
  Serial.print(F("WAVELENGTH:"));
  Serial.println(wavelength);
  Serial.print(F("PERIOD:"));
  Serial.println(period);
  Serial.print(F("DEADZONE:"));
  Serial.println(joyDeadzone);
  Serial.print(F("DEBOUNCE:"));
  Serial.println(clickDebounce);
  Serial.print(F("JOYSTICK:"));
  Serial.println(joystickEnabled ? "1" : "0");
  Serial.print(F("BASELINE:"));
  Serial.println(pressureBaseline);
  Serial.println(F("SETTINGS:END"));
}