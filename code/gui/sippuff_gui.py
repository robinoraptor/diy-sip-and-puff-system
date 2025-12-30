#!/usr/bin/env python3
"""
Sip & Puff Mouse Controller - GUI Configuration Tool
Echtzeit-Parameteranpassung über Serial-Verbindung
Modern UI mit CustomTkinter und Unicode-Symbolen
"""

import customtkinter as ctk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import threading
import json
import os
import sys
import time
from datetime import datetime

# PyInstaller-kompatible Pfad-Funktion
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# CustomTkinter Appearance
ctk.set_appearance_mode("system")  # "light" oder "dark"
ctk.set_default_color_theme(resource_path("theme_red.json"))  # Custom Red Theme

class SipPuffGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sip & Puff Controller - Einstellungen")
        self.root.geometry("650x850")
        self.root.resizable(False, True)
        
        # Serial-Verbindung
        self.serial_connection = None
        self.connected = False
        
        # Config-Dateien im User-Home-Verzeichnis (funktioniert auch in .app/.exe)
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".sippuff")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self.config_file = os.path.join(config_dir, "sippuff_config.json")
        self.default_config_file = os.path.join(config_dir, "sippuff_defaults.json")
        
        # Standard-Werte (werden aus JSON geladen)
        self.default_values = self.load_defaults()
        
        # Aktuelle Werte
        self.current_values = self.default_values.copy()
        
        # Unicode-Symbole
        self.icons = {
            'sync': '⟲',         # Sync-Pfeil
            'save': '⬇',         # Download/Save
            'undo': '↶',         # Zurück-Pfeil
            'refresh': '↻',      # Refresh-Pfeil
        }
        
        # Drucktest-Fenster
        self.pressure_test_window = None
        self.pressure_test_active = False
        self.pressure_update_pending = False  # Verhindere Update-Stau
        
        # Erweiterte Einstellungen ausklappbar
        self.advanced_expanded = False
        
        # Arduino Settings empfangen
        self.receiving_settings = False
        self.arduino_settings = {}
        
        self.create_widgets()
        self.load_config()
        
    def load_defaults(self):
        """Lädt Standard-Werte aus JSON oder erstellt die Datei"""
        default_values = {
            'click_left': 10,      
            'click_double': 15,    
            'click_right': -10,    
            'scroll_up': -5,       
            'scroll_down': 5,      
            'scroll_speed': 1,     
            'scroll_enabled': True,
            'wavelength': 15,
            'period': 35,
            'deadzone': 25,
            'debounce': 500,
            'joystick_enabled': True
        }
        
        # Prüfe ob Defaults-Datei existiert
        if os.path.exists(self.default_config_file):
            try:
                with open(self.default_config_file, 'r') as f:
                    loaded = json.load(f)
                    default_values.update(loaded)
                    print(f"✓ Standard-Werte aus {self.default_config_file} geladen")
            except Exception as e:
                print(f"⚠ Fehler beim Laden der Defaults: {e}")
        else:
            # Erstelle Defaults-Datei beim ersten Start
            try:
                with open(self.default_config_file, 'w') as f:
                    json.dump(default_values, f, indent=2)
                print(f"✓ Standard-Werte in {self.default_config_file} gespeichert")
            except Exception as e:
                print(f"⚠ Fehler beim Erstellen der Defaults-Datei: {e}")
        
        return default_values
        
    def create_widgets(self):
        # Header mit Titel 
        header = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        # Titel
        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left", fill="both", expand=True)
        
        title = ctk.CTkLabel(left_header, text="Sip & Puff Controller", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w")  
        
        subtitle = ctk.CTkLabel(left_header, text="Echtzeit-Konfiguration", font=ctk.CTkFont(size=12), text_color="gray")
        subtitle.pack(anchor="w")  
        
        # Drucktest-Button
        self.pressure_test_btn = ctk.CTkButton(header, text="Drucktest", 
                                              command=self.open_pressure_test,
                                              width=140,
                                              font=ctk.CTkFont(size=13, weight="bold"),
                                              state="disabled")  # Deaktiviert bis verbunden
        self.pressure_test_btn.pack(side="right", padx=5)
        
        # Scrollbarer Container für die einzelnen Blöcke
        scrollable_container = ctk.CTkScrollableFrame(self.root, corner_radius=10, fg_color="transparent")
        scrollable_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # scrollbarer Container
        main_frame = scrollable_container
        
        # Verbindungsbereich 
        conn_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        conn_frame.pack(fill="x", pady=(0, 10))
        
        conn_title = ctk.CTkLabel(conn_frame, text="Verbindung", font=ctk.CTkFont(size=16, weight="bold"))
        conn_title.grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(conn_frame, text="Port:").grid(row=1, column=0, sticky="w", padx=15, pady=10)
        
        self.port_combo = ctk.CTkComboBox(conn_frame, width=200, state="readonly")
        self.port_combo.grid(row=1, column=1, padx=10, pady=10)
        self.refresh_ports()
        
        self.refresh_btn = ctk.CTkButton(conn_frame, text=self.icons['refresh'], command=self.refresh_ports, width=40)
        self.refresh_btn.grid(row=1, column=2, padx=5, pady=10)
        
        self.connect_btn = ctk.CTkButton(conn_frame, text="Verbinden", command=self.toggle_connection, width=120)
        self.connect_btn.grid(row=1, column=3, padx=15, pady=10)
        
        self.status_label = ctk.CTkLabel(conn_frame, text="● Nicht verbunden", text_color="red", font=ctk.CTkFont(size=12, weight="bold"))
        self.status_label.grid(row=2, column=0, columnspan=4, padx=15, pady=(0, 15))
        
        # Klick-Schwellwerte
        click_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        click_frame.pack(fill="x", pady=(0, 10))
        
        click_title = ctk.CTkLabel(click_frame, text="Klick-Schwellwerte", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        click_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(15, 10))
        
        self.create_slider(click_frame, "Linksklick (Puff):", 'click_left', 0, 400, 1, tooltip="Pusten: Positiver Wert für Linksklick")
        self.create_slider(click_frame, "Doppelklick (Puff stark):", 'click_double', 0, 400, 2, tooltip="Stärkeres Pusten: Höherer positiver Wert für Doppelklick")
        self.create_slider(click_frame, "Rechtsklick (Sip):", 'click_right', -400, 0, 3, tooltip="Saugen: Negativer Wert für Rechtsklick")
        
        # Spacing
        ctk.CTkLabel(click_frame, text="").grid(row=4, column=0, pady=5)
        
        # Erweiterte Einstellungen (ausklappbar)
        advanced_container = ctk.CTkFrame(main_frame, corner_radius=10)
        advanced_container.pack(fill="x", pady=(0, 10))
        
        # Toggle-Header
        toggle_frame = ctk.CTkFrame(advanced_container, fg_color="transparent")
        toggle_frame.pack(fill="x", padx=15, pady=15)
        
        self.advanced_title = ctk.CTkLabel(toggle_frame, 
                                          text="▶ Erweiterte Einstellungen", 
                                          font=ctk.CTkFont(size=16, weight="bold"),
                                          cursor="hand2")
        self.advanced_title.pack(side="left")
        self.advanced_title.bind("<Button-1>", lambda e: self.toggle_advanced())
        
        # Info-Label
        self.advanced_info = ctk.CTkLabel(toggle_frame,
                                         text="(Klick zum Aufklappen)",
                                         font=ctk.CTkFont(size=11),
                                         text_color="gray")
        self.advanced_info.pack(side="left", padx=10)
        
        # Container für erweiterte Einstellungen (initial versteckt)
        self.advanced_content = ctk.CTkFrame(advanced_container, fg_color="transparent")
        
        # Scroll-Schwellwerte
        scroll_frame = ctk.CTkFrame(self.advanced_content, corner_radius=10, fg_color=("gray90", "gray25"))
        scroll_frame.pack(fill="x", pady=(0, 10), padx=15)
        
        scroll_title = ctk.CTkLabel(scroll_frame, text="Scroll-Schwellwerte", 
                                    font=ctk.CTkFont(size=14, weight="bold"))
        scroll_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(15, 10))
        
        # Checkbox für Scroll-Aktivierung
        self.scroll_var = ctk.BooleanVar(value=True)
        self.scroll_check = ctk.CTkCheckBox(scroll_frame, text="Scroll aktiviert", 
                                           variable=self.scroll_var,
                                           command=self.on_scroll_toggle,
                                           font=ctk.CTkFont(size=12, weight="bold"),
                                           border_width=1)
        self.scroll_check.grid(row=1, column=0, columnspan=3, sticky="w", padx=15, pady=10)
        
        self.create_slider(scroll_frame, "Scroll Up (Sip leicht):", 'scroll_up', -400, 0, 2, 
                          tooltip="Leichtes Saugen: Scrollt nach oben (sollte > Rechtsklick sein)")
        self.create_slider(scroll_frame, "Scroll Down (Puff leicht):", 'scroll_down', 0, 400, 3, 
                          tooltip="Leichtes Pusten: Scrollt nach unten (sollte < Linksklick sein)")
        self.create_slider(scroll_frame, "Scroll-Geschwindigkeit:", 'scroll_speed', 1, 5, 4, 
                          tooltip="Scroll-Speed: 1=langsam, 5=schnell")
        
        # Spacing
        ctk.CTkLabel(scroll_frame, text="").grid(row=5, column=0, pady=5)
        
        # Joystick-Schwellwerte
        joy_frame = ctk.CTkFrame(self.advanced_content, corner_radius=10, fg_color=("gray90", "gray25"))
        joy_frame.pack(fill="x", pady=(0, 10), padx=15)
        
        joy_title = ctk.CTkLabel(joy_frame, text="Joystick", font=ctk.CTkFont(size=14, weight="bold"))
        joy_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(15, 10))
        
        # Checkbox für Joystick-Aktivierung
        self.joystick_var = ctk.BooleanVar(value=True)
        self.joystick_check = ctk.CTkCheckBox(joy_frame, text="Joystick aktiviert", 
                                             variable=self.joystick_var,
                                             command=self.on_joystick_toggle,
                                             font=ctk.CTkFont(size=12, weight="bold"),
                                             border_width=1)
        self.joystick_check.grid(row=1, column=0, columnspan=3, sticky="w", padx=15, pady=10)
        
        self.create_slider(joy_frame, "Geschwindigkeit:", 'wavelength', 5, 50, 2, tooltip="Höher = schneller")
        self.create_slider(joy_frame, "Update-Rate (ms):", 'period', 10, 100, 3, tooltip="Kleiner = flüssiger (25-50 empfohlen)")
        self.create_slider(joy_frame, "Deadzone:", 'deadzone', 0, 100, 4, tooltip="Bereich ohne Bewegung um Mittelposition")
        
        # Spacing
        ctk.CTkLabel(joy_frame, text="").grid(row=5, column=0, pady=5)
        
        adv_frame = ctk.CTkFrame(self.advanced_content, corner_radius=10, fg_color=("gray90", "gray25"))
        adv_frame.pack(fill="x", pady=(0, 10), padx=15)
        
        adv_title = ctk.CTkLabel(adv_frame, text="Weitere Einstellungen", font=ctk.CTkFont(size=14, weight="bold"))
        adv_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(15, 10))
        
        self.create_slider(adv_frame, "Debounce (ms):", 'debounce', 100, 1000, 1, tooltip="Mindestzeit zwischen Klicks")
        
        # Spacing
        ctk.CTkLabel(adv_frame, text="").grid(row=2, column=0, pady=5)
        
        # Log-Bereich
        log_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        log_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        log_title = ctk.CTkLabel(log_frame, text="Aktionen & Status", font=ctk.CTkFont(size=16, weight="bold"))
        log_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        self.log_text = ctk.CTkTextbox(log_frame, height=120, font=ctk.CTkFont(size=11))
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Aktionsbuttons
        action_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.recal_btn = ctk.CTkButton(action_frame, text=f"{self.icons['sync']}  Rekalibrieren", 
                                      command=self.recalibrate, width=140, state="disabled",
                                      font=ctk.CTkFont(size=12))
        self.recal_btn.pack(side="left", padx=5)
        
        self.save_pc_btn = ctk.CTkButton(action_frame, text=f"{self.icons['save']}  Auf PC speichern", 
                                     command=self.save_config, width=140,
                                     font=ctk.CTkFont(size=12))
        self.save_pc_btn.pack(side="left", padx=5)
        
        self.save_arduino_btn = ctk.CTkButton(action_frame, text=f"💾  Auf Arduino speichern", 
                                     command=self.save_to_arduino, width=160, state="disabled",
                                     font=ctk.CTkFont(size=12),
                                     fg_color=("#2B8A3E", "#2B8A3E"),  # Grün
                                     hover_color=("#237A33", "#237A33"))
        self.save_arduino_btn.pack(side="left", padx=5)
        
        self.reset_btn = ctk.CTkButton(action_frame, text=f"{self.icons['undo']}  Standard", 
                                      command=self.reset_to_defaults, width=140,
                                      font=ctk.CTkFont(size=12))
        self.reset_btn.pack(side="left", padx=5)
        
    def create_slider(self, parent, label, key, from_, to, row, tooltip=""):
        ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=12)).grid(
            row=row, column=0, sticky="w", padx=15, pady=8)
        
        value_var = ctk.IntVar(value=self.current_values[key])
        
        # Slider 
        slider = ctk.CTkSlider(parent, from_=from_, to=to, 
                              variable=value_var, width=300,
                              command=lambda v: self.on_slider_change(key, v))
        slider.grid(row=row, column=1, padx=10, pady=8)
        
        # Editierbares Entry-Feld
        value_entry = ctk.CTkEntry(parent, width=70, justify="center", 
                                   font=ctk.CTkFont(size=12, weight="bold"))
        value_entry.insert(0, str(self.current_values[key]))
        value_entry.grid(row=row, column=2, padx=15, pady=8)
        
        # Event-Handler für manuelles Editieren
        def on_entry_change(event):
            try:
                new_value = int(value_entry.get())
                if from_ <= new_value <= to:
                    value_var.set(new_value)
                    self.current_values[key] = new_value
                    if self.connected:
                        self.send_setting(key, new_value)
                else:
                    value_entry.delete(0, "end")
                    value_entry.insert(0, str(self.current_values[key]))
            except ValueError:
                value_entry.delete(0, "end")
                value_entry.insert(0, str(self.current_values[key]))
        
        value_entry.bind("<Return>", on_entry_change)
        value_entry.bind("<FocusOut>", on_entry_change)
        
        # Tooltip
        if tooltip:
            self.create_tooltip(slider, tooltip)
        
        # Speichere Referenzen
        setattr(self, f"{key}_var", value_var)
        setattr(self, f"{key}_entry", value_entry)
        
    def create_tooltip(self, widget, text):
        def on_enter(event):
            tooltip = ctk.CTkToplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            tooltip.attributes('-topmost', True)
            label = ctk.CTkLabel(tooltip, text=text, 
                                font=ctk.CTkFont(size=11), 
                                corner_radius=6,
                                fg_color=("#333333", "#222222"),
                                text_color="white")  # Weißer Text
            label.pack(padx=10, pady=5)
            widget.tooltip = tooltip
            
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        
    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        if ports:
            self.port_combo.configure(values=ports)
            self.port_combo.set(ports[0])
        else:
            self.port_combo.configure(values=["Keine Ports gefunden"])
            self.port_combo.set("Keine Ports gefunden")
            
    def toggle_connection(self):
        if not self.connected:
            self.connect()
        else:
            self.disconnect()
            
    def connect(self):
        port = self.port_combo.get()
        if not port or port == "Keine Ports gefunden":
            messagebox.showerror("Fehler", "Bitte wähle einen Port aus!")
            return
            
        try:
            self.serial_connection = serial.Serial(port, 115200, timeout=1)
            self.connected = True
            self.connect_btn.configure(text="Trennen")
            self.status_label.configure(text="● Verbunden", text_color="green")
            self.recal_btn.configure(state="normal")
            self.pressure_test_btn.configure(state="normal")  # Drucktest aktivieren
            self.save_arduino_btn.configure(state="normal")  # Arduino-Speicher aktivieren
            self.log(f"Verbunden mit {port}")
            
            # Starte Empfangs-Thread
            self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.read_thread.start()
            
            # Arduino sendet automatisch seine Settings beim Start
            self.log("Warte auf Arduino-Einstellungen...")
            
        except Exception as e:
            messagebox.showerror("Verbindungsfehler", f"Konnte nicht verbinden: {e}")
            self.log(f"Fehler: {e}")
            
    def disconnect(self):
        if self.serial_connection:
            # Drucktest stoppen falls aktiv
            if self.pressure_test_active:
                self.close_pressure_test()
            
            self.serial_connection.close()
            self.connected = False
            self.connect_btn.configure(text="Verbinden")
            self.status_label.configure(text="● Nicht verbunden", text_color="red")
            self.recal_btn.configure(state="disabled")
            self.pressure_test_btn.configure(state="disabled")  # Drucktest deaktivieren
            self.save_arduino_btn.configure(state="disabled")  # Arduino-Speicher deaktivieren
            self.log("Verbindung getrennt")
            
    def read_serial(self):
        while self.connected and self.serial_connection:
            try:
                if self.serial_connection.in_waiting:
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    # WICHTIG: Entferne auch \r explizit (Windows Line Endings)
                    line = line.replace('\r', '').replace('\n', '')
                    if line:
                        # Debug-Ausgabe nur wenn NICHT im Drucktest (zu viel Output)
                        if not self.pressure_test_active:
                            print(f"DEBUG read_serial: '{line}'")
                        self.process_serial_message(line)
            except Exception as e:
                self.log(f"Lesefehler: {e}")
                break
                
    def process_serial_message(self, msg):
        # Im Drucktest-Modus: Interpretiere jede Zeile direkt als Zahl
        if self.pressure_test_active:
            try:
                # Versuche direkt als Zahl zu parsen
                pressure_value = int(msg.strip())
                
                # Throttling: Nur updaten wenn kein Update läuft
                if not self.pressure_update_pending:
                    self.pressure_update_pending = True
                    self.root.after(0, self._do_pressure_update, pressure_value)
                
                return  
            except ValueError:
                pass
        
        # Normale Verarbeitung (außerhalb Drucktest)
        if msg.startswith("ACTION:"):
            action = msg.split(":")[1]
            action_names = {
                'LEFT_CLICK': '→ Linksklick',
                'DOUBLE_CLICK': '→→ Doppelklick',
                'RIGHT_CLICK': '→ Rechtsklick'
            }
            self.log(action_names.get(action, action))
        elif msg.startswith("OK:"):
            # Bestätigung erhalten
            if "PRESSURE_TEST" in msg:
                print(f"DEBUG: {msg}")
        elif msg.startswith("INFO:"):
            info = msg.split(":", 1)[1]
            self.log(f"ℹ {info}")
        elif msg.startswith("SETTINGS:"):
            # Arduino-Einstellungen empfangen
            if msg == "SETTINGS:START":
                self.receiving_settings = True
                self.arduino_settings = {}
            elif msg == "SETTINGS:END":
                self.receiving_settings = False
                self.root.after(0, self.apply_arduino_settings)
            elif self.receiving_settings:
                try:
                    parts = msg.replace("SETTINGS:", "").split(":", 1)
                    if len(parts) == 2:
                        key, value = parts
                        self.arduino_settings[key] = value
                except:
                    pass
        else:
            # Andere Nachrichten loggen
            self.log(msg)
                
    def on_slider_change(self, key, value):
        value = int(float(value))
        self.current_values[key] = value
        
        # Update Entry-Feld
        entry = getattr(self, f"{key}_entry")
        entry.delete(0, "end")
        entry.insert(0, str(value))
        
        if self.connected:
            self.send_setting(key, value)
            
    def on_joystick_toggle(self):
        enabled = self.joystick_var.get()
        self.current_values['joystick_enabled'] = enabled
        
        if self.connected:
            self.send_setting('joystick', 1 if enabled else 0)
            self.log(f"Joystick {'aktiviert' if enabled else 'deaktiviert'}")
    
    def on_scroll_toggle(self):
        enabled = self.scroll_var.get()
        self.current_values['scroll_enabled'] = enabled
        
        if self.connected:
            self.send_setting('scroll', 1 if enabled else 0)
            self.log(f"Scroll {'aktiviert' if enabled else 'deaktiviert'}")
            
    def send_setting(self, key, value):
        if not self.connected or not self.serial_connection:
            return
            
        key_map = {
            'click_left': 'CLICK_LEFT',
            'click_double': 'CLICK_DOUBLE',
            'click_right': 'CLICK_RIGHT',
            'scroll_up': 'SCROLL_UP',       
            'scroll_down': 'SCROLL_DOWN',   
            'scroll_speed': 'SCROLL_SPEED', 
            'scroll': 'SCROLL',
            'wavelength': 'WAVELENGTH',
            'period': 'PERIOD',
            'deadzone': 'DEADZONE',
            'debounce': 'DEBOUNCE',
            'joystick': 'JOYSTICK'
        }
        
        arduino_key = key_map.get(key, key.upper())
        command = f"SET:{arduino_key}:{value}\n"
        
        try:
            self.serial_connection.write(command.encode())
        except Exception as e:
            self.log(f"Sendefehler: {e}")
            
    def sync_all_settings(self):
        """Sendet alle aktuellen Einstellungen an Arduino"""
        for key, value in self.current_values.items():
            if key == 'joystick_enabled':
                self.send_setting('joystick', 1 if value else 0)
            elif key == 'scroll_enabled':
                self.send_setting('scroll', 1 if value else 0)
            else:
                self.send_setting(key, value)
        self.log("Einstellungen synchronisiert")
        
    def recalibrate(self):
        if not self.connected:
            return
            
        try:
            self.serial_connection.write(b"RECALIBRATE\n")
            self.log("Rekalibrierung gestartet...")
        except Exception as e:
            self.log(f"Fehler: {e}")
            
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.current_values, f, indent=2)
            self.log("✓ Einstellungen auf PC gespeichert")
            messagebox.showinfo("Gespeichert", "Einstellungen wurden auf dem PC gespeichert!")
        except Exception as e:
            self.log(f"Speicherfehler: {e}")
            messagebox.showerror("Fehler", f"Konnte nicht speichern: {e}")
    
    def save_to_arduino(self):
        """Speichert aktuelle Einstellungen im Arduino EEPROM"""
        if not self.connected:
            return
        
        result = messagebox.askyesno(
            "Auf Arduino speichern",
            "Möchtest du die aktuellen Einstellungen im Arduino speichern?\n\n"
            "Vorteil: Arduino funktioniert ohne PC/GUI\n"
            "Die Einstellungen bleiben auch nach Neustart erhalten"
        )
        
        if result:
            try:
                # Erst alle Einstellungen senden
                self.sync_all_settings()
                time.sleep(0.5)  # Warte bis alle Einstellungen übertragen sind
                
                # Dann im EEPROM speichern
                self.serial_connection.write(b"SAVE_EEPROM\n")
                self.log("💾 Speichere Einstellungen im Arduino...")
                
                # Warte auf Bestätigung
                time.sleep(1)
                
                messagebox.showinfo(
                    "Erfolg!", 
                    "Einstellungen wurden im Arduino gespeichert!\n\n"
                    "Arduino funktioniert jetzt Plug & Play\n"
                    "Auch ohne PC/GUI"
                )
                
            except Exception as e:
                self.log(f"Fehler beim Speichern: {e}")
                messagebox.showerror("Fehler", f"Konnte nicht im Arduino speichern: {e}")
            
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    self.current_values.update(loaded)
                    self.update_ui_from_values()
                    self.log("Gespeicherte Einstellungen geladen")
            except Exception as e:
                self.log(f"Ladefehler: {e}")
                
    def reset_to_defaults(self):
        if messagebox.askyesno("Zurücksetzen", 
                              "Möchtest du alle Einstellungen auf Standard zurücksetzen?"):
            # Lade Defaults neu aus JSON
            self.default_values = self.load_defaults()
            self.current_values = self.default_values.copy()
            self.update_ui_from_values()
            
            if self.connected:
                self.sync_all_settings()
                
            self.log("Auf Standard zurückgesetzt")
            
    def update_ui_from_values(self):
        for key, value in self.current_values.items():
            if key == 'joystick_enabled':
                self.joystick_var.set(value)
            elif key == 'scroll_enabled':
                self.scroll_var.set(value)
            elif hasattr(self, f"{key}_var"):
                var = getattr(self, f"{key}_var")
                var.set(value)
                entry = getattr(self, f"{key}_entry")
                entry.delete(0, "end")
                entry.insert(0, str(value))
    
    def _do_pressure_update(self, pressure_value):
        """Führt das Drucktest-Update aus und setzt Flag zurück"""
        try:
            self.update_pressure_display(pressure_value)
        finally:
            # Flag zurücksetzen - bereit für nächstes Update
            self.pressure_update_pending = False
    
    def toggle_advanced(self):
        """Klappt erweiterte Einstellungen ein/aus"""
        self.advanced_expanded = not self.advanced_expanded
        
        if self.advanced_expanded:
            # Aufklappen
            self.advanced_title.configure(text="▼ Erweiterte Einstellungen")
            self.advanced_info.configure(text="(Klick zum Zuklappen)")
            self.advanced_content.pack(fill="x", pady=(0, 15))
        else:
            # Zuklappen
            self.advanced_title.configure(text="▶ Erweiterte Einstellungen")
            self.advanced_info.configure(text="(Klick zum Aufklappen)")
            self.advanced_content.pack_forget()
    
    def apply_arduino_settings(self):
        """Übernimmt Einstellungen vom Arduino in die GUI"""
        key_map = {
            'CLICK_LEFT': 'click_left',
            'CLICK_DOUBLE': 'click_double',
            'CLICK_RIGHT': 'click_right',
            'SCROLL_UP': 'scroll_up',
            'SCROLL_DOWN': 'scroll_down',
            'SCROLL_SPEED': 'scroll_speed',
            'SCROLL': 'scroll_enabled',
            'WAVELENGTH': 'wavelength',
            'PERIOD': 'period',
            'DEADZONE': 'deadzone',
            'DEBOUNCE': 'debounce',
            'JOYSTICK': 'joystick_enabled'
        }
        
        settings_updated = False
        
        for arduino_key, value_str in self.arduino_settings.items():
            if arduino_key in key_map:
                gui_key = key_map[arduino_key]
                
                try:
                    if gui_key in ['scroll_enabled', 'joystick_enabled']:
                        value = (value_str == '1' or value_str.upper() == 'TRUE')
                    else:
                        value = int(value_str)
                    
                    self.current_values[gui_key] = value
                    settings_updated = True
                except:
                    pass
        
        if settings_updated:
            self.update_ui_from_values()
            self.log("✓ Einstellungen vom Arduino geladen")
    
    def open_pressure_test(self):
        """Öffnet das Drucktest-Fenster"""
        if self.pressure_test_window is not None and self.pressure_test_window.winfo_exists():
            self.pressure_test_window.focus()
            return
        
        # Starte Drucktest-Modus am Arduino
        if self.connected and self.serial_connection:
            try:
                self.serial_connection.reset_input_buffer()  # Empfangsbuffer leeren
                self.serial_connection.reset_output_buffer()  # Sendebuffer leeren
                print("DEBUG: Serial Buffer geleert")
                
                time.sleep(0.1)
                
                # Starte Drucktest
                self.serial_connection.write(b"PRESSURE_TEST:START\n")
                self.pressure_test_active = True
                print("DEBUG: PRESSURE_TEST:START gesendet")
            except Exception as e:
                self.log(f"Fehler beim Starten des Drucktests: {e}")
                return
        
        # Erstelle neues Toplevel-Fenster
        self.pressure_test_window = ctk.CTkToplevel(self.root)
        self.pressure_test_window.title("Drucktest - Echtzeit-Anzeige")
        self.pressure_test_window.geometry("500x400")
        self.pressure_test_window.resizable(False, False)
        
        # Wenn Fenster geschlossen wird, Drucktest stoppen
        self.pressure_test_window.protocol("WM_DELETE_WINDOW", self.close_pressure_test)
        
        # Titel
        title_label = ctk.CTkLabel(self.pressure_test_window, 
                                   text="Drucktest", 
                                   font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Info-Text
        info_label = ctk.CTkLabel(self.pressure_test_window,
                                  text="Puste oder sauge in den Schlauch, um den Druck zu testen",
                                  font=ctk.CTkFont(size=12),
                                  text_color="gray")
        info_label.pack(pady=(0, 20))
        
        # Haupt-Container für Druckwert
        self.pressure_display_frame = ctk.CTkFrame(self.pressure_test_window, 
                                                   corner_radius=15,
                                                   fg_color=("gray85", "gray20"))
        self.pressure_display_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Großer Druckwert-Label
        self.pressure_value_label = ctk.CTkLabel(self.pressure_display_frame,
                                                 text="0",
                                                 font=ctk.CTkFont(size=80, weight="bold"))
        self.pressure_value_label.pack(pady=(40, 10))
        
        # Status-Label (NEUTRAL, SAUGEN, PUSTEN)
        self.pressure_status_label = ctk.CTkLabel(self.pressure_display_frame,
                                                  text="NEUTRAL",
                                                  font=ctk.CTkFont(size=24, weight="bold"))
        self.pressure_status_label.pack(pady=(0, 20))
        
        # Progressbar als visuelle Darstellung
        self.pressure_progress = ctk.CTkProgressBar(self.pressure_display_frame,
                                                    width=400,
                                                    height=20)
        self.pressure_progress.pack(pady=(0, 40))
        self.pressure_progress.set(0.5)  # Mitte = Neutral
        
        # Schließen-Button
        close_btn = ctk.CTkButton(self.pressure_test_window,
                                  text="Schließen",
                                  command=self.close_pressure_test,
                                  width=150,
                                  font=ctk.CTkFont(size=14))
        close_btn.pack(pady=(0, 20))
        
        self.log("Drucktest gestartet")
    
    def close_pressure_test(self):
        """Schließt das Drucktest-Fenster und stoppt den Test"""
        if self.connected and self.serial_connection and self.pressure_test_active:
            try:
                self.serial_connection.write(b"PRESSURE_TEST:STOP\n")
                self.pressure_test_active = False
                self.pressure_update_pending = False  # Flag zurücksetzen
                print("DEBUG: PRESSURE_TEST:STOP gesendet")
                
                # Warte kurz und leere dann den Buffer
                time.sleep(0.2)
                self.serial_connection.reset_input_buffer()
                print("DEBUG: Serial Buffer nach Stop geleert")
            except Exception as e:
                self.log(f"Fehler beim Stoppen des Drucktests: {e}")
        
        if self.pressure_test_window is not None and self.pressure_test_window.winfo_exists():
            self.pressure_test_window.destroy()
            self.pressure_test_window = None
        
        self.log("Drucktest beendet")
    
    def update_pressure_display(self, pressure_value):
        """Aktualisiert die Drucktest-Anzeige"""
        
        if self.pressure_test_window is None:
            return
        
        if not self.pressure_test_window.winfo_exists():
            return
        
        # Update Wert-Label
        self.pressure_value_label.configure(text=str(pressure_value))
        
        # Bestimme Status und Farbe
        if pressure_value < -5:
            # Saugen
            status = "SAUGEN"
            color = "#3498db"  # Blau
            progress_value = max(0, 0.5 - abs(pressure_value) / 800)  # Links von Mitte
        elif pressure_value > 5:
            # Pusten
            status = "PUSTEN"
            color = "#e74c3c"  # Rot
            progress_value = min(1.0, 0.5 + abs(pressure_value) / 800)  # Rechts von Mitte
        else:
            # Neutral
            status = "NEUTRAL"
            color = "#2ecc71"  # Grün
            progress_value = 0.5
        
        # Update Status-Label
        self.pressure_status_label.configure(text=status, text_color=color)
        self.pressure_value_label.configure(text_color=color)
        
        # Update Progressbar
        self.pressure_progress.set(progress_value)
                
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")

def main():
    root = ctk.CTk()
    app = SipPuffGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()