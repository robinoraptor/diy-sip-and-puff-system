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
from datetime import datetime

# CustomTkinter Appearance
ctk.set_appearance_mode("system")  # "light" oder "dark"
ctk.set_default_color_theme("theme_red.json")  # "blue", "green", "dark-blue"

class SipPuffGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sip & Puff Controller - Einstellungen")
        self.root.geometry("650x800")
        self.root.resizable(False, True)  # Fenster nicht veränderbar
        
        # Serial-Verbindung
        self.serial_connection = None
        self.connected = False
        self.config_file = "sippuff_config.json"
        self.default_config_file = "sippuff_defaults.json"
        
        # Standard-Werte (werden aus JSON geladen)
        self.default_values = self.load_defaults()
        
        # Aktuelle Werte
        self.current_values = self.default_values.copy()
        
        # Unicode-Symbole (besser als Emojis, funktionieren überall)
        self.icons = {
            'gamepad': '⬢',      # Sechseck für Gaming
            'wifi': '◈',         # Netzwerk-Symbol
            'mouse': '◉',        # Gefüllter Kreis für Klicks
            'cog': '⚙',          # Zahnrad
            'clipboard': '◫',    # Clipboard
            'sync': '⟲',         # Sync-Pfeil
            'save': '⬇',         # Download/Save
            'undo': '↶',         # Zurück-Pfeil
            'refresh': '↻',      # Refresh-Pfeil
        }
        
        self.create_widgets()
        self.load_config()
        
    def load_defaults(self):
        """Lädt Standard-Werte aus JSON oder erstellt die Datei"""
        default_values = {
            'click_left': -10,
            'click_double': -15,
            'click_right': 10,
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
                # Verwende hardcoded defaults
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
        # Header mit Titel - linksbündig
        header = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(header, text="Sip & Puff Controller", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w")  # Linksbündig
        
        subtitle = ctk.CTkLabel(header, text="Echtzeit-Konfiguration", font=ctk.CTkFont(size=12), text_color="gray")
        subtitle.pack(anchor="w")  # Linksbündig
        
        # Scrollbarer Container (WEISS) für die einzelnen Blöcke
        scrollable_container = ctk.CTkScrollableFrame(self.root, corner_radius=10, fg_color="transparent")
        scrollable_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # main_frame ist jetzt der scrollbare Container
        main_frame = scrollable_container
        
        # Verbindungsbereich (einzelner Block)
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
        
        self.create_slider(click_frame, "Linksklick (Sip):", 'click_left', -400, 0, 1, tooltip="Saugen: Negativer Wert für Linksklick")
        self.create_slider(click_frame, "Doppelklick (Sip stark):", 'click_double', -400, 0, 2, tooltip="Stärkeres Saugen: Noch negativer für Doppelklick")
        self.create_slider(click_frame, "Rechtsklick (Puff):", 'click_right', 0, 400, 3, tooltip="Blasen: Positiver Wert für Rechtsklick")
        
        # Spacing
        ctk.CTkLabel(click_frame, text="").grid(row=4, column=0, pady=5)
        
        # Joystick-Einstellungen
        joy_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        joy_frame.pack(fill="x", pady=(0, 10))
        
        joy_title = ctk.CTkLabel(joy_frame, text="Joystick", font=ctk.CTkFont(size=16, weight="bold"))
        joy_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(15, 10))
        
        # Checkbox für Joystick-Aktivierung
        self.joystick_var = ctk.BooleanVar(value=True)
        self.joystick_check = ctk.CTkCheckBox(joy_frame, text="Joystick aktiviert", 
                                             variable=self.joystick_var,
                                             command=self.on_joystick_toggle,
                                             font=ctk.CTkFont(size=13, weight="bold"),
                                             border_width=1)  # Dünner Rahmen
        self.joystick_check.grid(row=1, column=0, columnspan=3, sticky="w", padx=15, pady=10)
        
        self.create_slider(joy_frame, "Geschwindigkeit:", 'wavelength', 5, 50, 2, tooltip="Höher = schneller")
        self.create_slider(joy_frame, "Update-Rate (ms):", 'period', 10, 100, 3, tooltip="Kleiner = flüssiger (25-50 empfohlen)")
        self.create_slider(joy_frame, "Deadzone:", 'deadzone', 0, 100, 4, tooltip="Bereich ohne Bewegung um Mittelposition")
        
        # Spacing
        ctk.CTkLabel(joy_frame, text="").grid(row=5, column=0, pady=5)
        
        # Erweiterte Einstellungen
        adv_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        adv_frame.pack(fill="x", pady=(0, 10))
        
        adv_title = ctk.CTkLabel(adv_frame, text="Erweitert", font=ctk.CTkFont(size=16, weight="bold"))
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
        
        # Aktionsbuttons - AUSSERHALB, im freien Raum mit Text UND Icons
        action_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.recal_btn = ctk.CTkButton(action_frame, text=f"{self.icons['sync']}  Rekalibrieren", 
                                      command=self.recalibrate, width=180, state="disabled",
                                      font=ctk.CTkFont(size=13))
        self.recal_btn.pack(side="left", padx=5)
        
        self.save_btn = ctk.CTkButton(action_frame, text=f"{self.icons['save']}  Speichern", 
                                     command=self.save_config, width=180,
                                     font=ctk.CTkFont(size=13))
        self.save_btn.pack(side="left", padx=5)
        
        self.reset_btn = ctk.CTkButton(action_frame, text=f"{self.icons['undo']}  Standard", 
                                      command=self.reset_to_defaults, width=180,
                                      font=ctk.CTkFont(size=13))
        self.reset_btn.pack(side="left", padx=5)
        
    def create_slider(self, parent, label, key, from_, to, row, tooltip=""):
        ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=12)).grid(
            row=row, column=0, sticky="w", padx=15, pady=8)
        
        value_var = ctk.IntVar(value=self.current_values[key])
        
        # Slider mit angepassten Farben
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
                    # Wert außerhalb des Bereichs - zurücksetzen
                    value_entry.delete(0, "end")
                    value_entry.insert(0, str(self.current_values[key]))
            except ValueError:
                # Ungültige Eingabe - zurücksetzen
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
            self.log(f"Verbunden mit {port}")
            
            # Starte Empfangs-Thread
            self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.read_thread.start()
            
            # Sende aktuelle Einstellungen
            self.root.after(1000, self.sync_all_settings)
            
        except Exception as e:
            messagebox.showerror("Verbindungsfehler", f"Konnte nicht verbinden: {e}")
            self.log(f"Fehler: {e}")
            
    def disconnect(self):
        if self.serial_connection:
            self.serial_connection.close()
            self.connected = False
            self.connect_btn.configure(text="Verbinden")
            self.status_label.configure(text="● Nicht verbunden", text_color="red")
            self.recal_btn.configure(state="disabled")
            self.log("Verbindung getrennt")
            
    def read_serial(self):
        while self.connected and self.serial_connection:
            try:
                if self.serial_connection.in_waiting:
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    if line:
                        self.process_serial_message(line)
            except Exception as e:
                self.log(f"Lesefehler: {e}")
                break
                
    def process_serial_message(self, msg):
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
            pass
        elif msg.startswith("INFO:"):
            info = msg.split(":", 1)[1]
            self.log(f"ℹ {info}")
        else:
            # Andere Nachrichten loggen
            if not msg.startswith("SETTINGS:"):
                self.log(msg)
                
    def on_slider_change(self, key, value):
        value = int(float(value))
        self.current_values[key] = value
        
        # Update Entry-Feld
        entry = getattr(self, f"{key}_entry")
        entry.delete(0, "end")
        entry.insert(0, str(value))
        
        # Sende an Arduino (wenn verbunden)
        if self.connected:
            self.send_setting(key, value)
            
    def on_joystick_toggle(self):
        enabled = self.joystick_var.get()
        self.current_values['joystick_enabled'] = enabled
        
        if self.connected:
            self.send_setting('joystick', 1 if enabled else 0)
            self.log(f"Joystick {'aktiviert' if enabled else 'deaktiviert'}")
            
    def send_setting(self, key, value):
        if not self.connected or not self.serial_connection:
            return
            
        key_map = {
            'click_left': 'CLICK_LEFT',
            'click_double': 'CLICK_DOUBLE',
            'click_right': 'CLICK_RIGHT',
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
            self.log("✓ Einstellungen gespeichert")
            messagebox.showinfo("Gespeichert", "Einstellungen wurden erfolgreich gespeichert!")
        except Exception as e:
            self.log(f"Speicherfehler: {e}")
            messagebox.showerror("Fehler", f"Konnte nicht speichern: {e}")
    
    def save_as_defaults(self):
        """Speichert aktuelle Werte als neue Standard-Werte"""
        if messagebox.askyesno("Als Standard speichern", 
                              "Möchtest du die aktuellen Einstellungen als neue Standard-Werte speichern?\n\n"
                              "Diese werden beim Klick auf 'Standard' wiederhergestellt."):
            try:
                with open(self.default_config_file, 'w') as f:
                    json.dump(self.current_values, f, indent=2)
                self.default_values = self.current_values.copy()
                self.log("✓ Als Standard gespeichert")
                messagebox.showinfo("Gespeichert", "Aktuelle Einstellungen wurden als neue Standard-Werte gespeichert!")
            except Exception as e:
                self.log(f"Fehler beim Speichern der Defaults: {e}")
                messagebox.showerror("Fehler", f"Konnte Defaults nicht speichern: {e}")
            
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
            # Lade Defaults neu aus JSON (falls sie geändert wurden)
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
            elif hasattr(self, f"{key}_var"):
                var = getattr(self, f"{key}_var")
                var.set(value)
                entry = getattr(self, f"{key}_entry")
                entry.delete(0, "end")
                entry.insert(0, str(value))
                
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