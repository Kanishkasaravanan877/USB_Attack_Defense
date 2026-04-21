# -*- coding: utf-8 -*-
"""
USB Attack Simulation vs Device Control Defense
Cyber Range as a Service - Attack-Defense Simulation
Author: Student Submission
Description: GUI-based simulation demonstrating USB-based attack vectors
             and corresponding defense mechanisms using device control policies.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
import hashlib
import os
import json
from datetime import datetime
from collections import defaultdict


# --------------------------- Color Palette --------------------------------
BG_DARK     = "#0d1117"
BG_PANEL    = "#161b22"
BG_CARD     = "#21262d"
ACCENT_RED  = "#ff4444"
ACCENT_BLUE = "#58a6ff"
ACCENT_GRN  = "#3fb950"
ACCENT_YEL  = "#d29922"
ACCENT_PUR  = "#bc8cff"
TEXT_MAIN   = "#e6edf3"
TEXT_SUB    = "#8b949e"
BORDER      = "#30363d"


# ----------------------- Attack Simulation Engine -------------------------
class USBAttackEngine:
    """Simulates various USB-based attack vectors."""

    ATTACK_TYPES = {
        "BadUSB / HID Injection": {
            "description": "Emulates a keyboard/HID device to inject malicious keystrokes.",
            "payload": [
                "Enumerating as HID device (VID:0x046D PID:0xC52B)...",
                "Injecting keystrokes: WIN+R -> cmd.exe",
                "Executing: powershell -w hidden -enc <BASE64_PAYLOAD>",
                "Downloading reverse shell payload from C2 server...",
                "Establishing persistent backdoor via registry run key...",
                "Exfiltrating credential dump (SAM hive)...",
            ],
            "severity": "CRITICAL",
            "color": ACCENT_RED,
            "mitre": "T1200 - Hardware Additions, T1059.001 - PowerShell",
        },
        "Rubber Ducky Script": {
            "description": "USB device that automates keystroke injection via Ducky Script.",
            "payload": [
                "USB Rubber Ducky detected by host OS as HID keyboard...",
                "Executing Ducky Script payload (delay 500ms)...",
                "Opening browser -> navigating to phishing page...",
                "Stealing saved browser credentials (Chrome/Edge profiles)...",
                "Copying credential database to USB mass storage...",
                "Clearing PowerShell event logs to avoid detection...",
            ],
            "severity": "HIGH",
            "color": ACCENT_RED,
            "mitre": "T1056.001 - Keylogging, T1555.003 - Browser Creds",
        },
        "USB Drop / Autorun Malware": {
            "description": "Malware planted on USB that auto-executes on plug-in via autorun.inf.",
            "payload": [
                "USB mass storage device inserted (32GB, FAT32)...",
                "autorun.inf detected -> executing setup.exe...",
                "Dropping malware to C:\\Users\\Public\\svchost.exe...",
                "Creating persistence via HKCU\\Run registry key...",
                "Scanning internal network: 192.168.1.0/24...",
                "Lateral movement initiated via SMB (EternalBlue)...",
            ],
            "severity": "HIGH",
            "color": ACCENT_YEL,
            "mitre": "T1091 - Replication Through Removable Media",
        },
        "USB Killer (Electrical)": {
            "description": "Sends high-voltage power surges to destroy hardware components.",
            "payload": [
                "USB Killer device detected (VID:0x0000 PID:0x0001)...",
                "Charging capacitors to 200V DC...",
                "Discharging surge voltage into USB data lines...",
                "USB controller fried -- hardware damage confirmed.",
                "Motherboard northbridge potentially damaged.",
                "System unresponsive -- hardware DoS achieved.",
            ],
            "severity": "CRITICAL",
            "color": ACCENT_RED,
            "mitre": "T1485 - Data Destruction (Hardware)",
        },
        "Data Exfiltration via USB": {
            "description": "Covertly copies sensitive files to an unauthorized USB device.",
            "payload": [
                "Unauthorized mass storage detected (unlisted in whitelist)...",
                "Enumerating target directories: /Documents, /Desktop...",
                "Found 47 sensitive files (*.docx, *.pdf, *.xlsx)...",
                "Copying 2.3 GB of data to USB drive (throttled to avoid alerts)...",
                "Data exfiltrated: financials.xlsx, passwords.kdbx, contracts/...",
                "Wiping USB access timestamps using timestomping...",
            ],
            "severity": "HIGH",
            "color": ACCENT_YEL,
            "mitre": "T1052.001 - Exfiltration over USB",
        },
        "Fake USB Charging Cable (O.MG)": {
            "description": "Weaponized USB cable with embedded WiFi implant for remote access.",
            "payload": [
                "O.MG Cable connected -- appears as standard USB cable...",
                "Embedded ARM processor booting internal firmware...",
                "WiFi access point activated (SSID: iPhone Hotspot)...",
                "Receiving commands from attacker over HTTP/2...",
                "Injecting keystrokes: establishing reverse TCP shell...",
                "Attacker has full remote control via cable implant.",
            ],
            "severity": "CRITICAL",
            "color": ACCENT_PUR,
            "mitre": "T1200 - Hardware Additions, T1021 - Remote Services",
        },
    }

    def __init__(self):
        self.active = False

    def run_attack(self, attack_name, log_callback, status_callback, progress_callback):
        """Execute the selected attack simulation step-by-step."""
        attack = self.ATTACK_TYPES[attack_name]
        self.active = True
        payload = attack["payload"]

        status_callback(f"[!] ATTACK RUNNING: {attack_name}", attack["color"])

        for i, step in enumerate(payload):
            if not self.active:
                break
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            log_callback(f"[{timestamp}] [ATTACK] {step}", attack["color"])
            progress_callback(int((i + 1) / len(payload) * 100))
            time.sleep(random.uniform(0.6, 1.4))

        if self.active:
            log_callback(f"\n{'-'*60}", attack["color"])
            log_callback(f"[ATTACK COMPLETE] Severity: {attack['severity']}", attack["color"])
            log_callback(f"[MITRE ATT&CK]   {attack['mitre']}", ACCENT_YEL)
            log_callback(f"{'-'*60}\n", attack["color"])
            status_callback(f"[!!] ATTACK SUCCEEDED -- {attack_name}", ACCENT_RED)
        self.active = False

    def stop(self):
        self.active = False


# ----------------------- Defense Engine -----------------------------------
class DeviceControlDefense:
    """Simulates USB device control defense mechanisms."""

    DEFENSE_POLICIES = {
        "USB Port Blocking": {
            "description": "Disables all USB ports at OS/hardware level via Group Policy.",
            "steps": [
                "Loading Device Control Policy from GPO...",
                "Applying registry key: HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR -> Start=4",
                "USB Storage class driver (USBSTOR) disabled system-wide.",
                "Blocking HID class devices (non-trusted)...",
                "Policy enforced on all 8 USB ports.",
                "Alert sent to SIEM: USB block policy active.",
            ],
            "blocks": ["BadUSB / HID Injection", "Rubber Ducky Script", "USB Drop / Autorun Malware",
                       "Data Exfiltration via USB", "Fake USB Charging Cable (O.MG)"],
        },
        "Device Whitelisting": {
            "description": "Allow only pre-approved USB devices by VID/PID or serial number.",
            "steps": [
                "Loading approved device whitelist (42 trusted devices)...",
                "Monitoring USB bus for new device enumeration...",
                "Comparing VID/PID against whitelist database...",
                "Device VID:0x046D PID:0xC52B -> NOT IN WHITELIST.",
                "Blocking unauthorized device -- port access denied.",
                "Incident logged in USB audit log with device fingerprint.",
            ],
            "blocks": ["BadUSB / HID Injection", "Rubber Ducky Script", "USB Drop / Autorun Malware",
                       "Data Exfiltration via USB", "Fake USB Charging Cable (O.MG)", "USB Killer (Electrical)"],
        },
        "Endpoint DLP (Data Loss Prevention)": {
            "description": "Monitors and blocks unauthorized data transfer to USB storage.",
            "steps": [
                "DLP agent active -- monitoring file system events...",
                "USB mass storage connected: Volume D:\\ detected.",
                "Scanning files queued for transfer...",
                "ALERT: Sensitive content detected (PII, financial data).",
                "Transfer blocked -- 47 files quarantined.",
                "DLP incident report generated (Ref: DLP-2024-0891).",
            ],
            "blocks": ["Data Exfiltration via USB", "USB Drop / Autorun Malware"],
        },
        "Physical USB Port Guard": {
            "description": "Hardware-level physical port blockers prevent physical access.",
            "steps": [
                "Hardware port locks installed on all USB-A/C ports.",
                "Tamper-detection sensor armed on each port lock.",
                "Unauthorized insertion attempt detected on Port #3...",
                "Physical alarm triggered -- security notified.",
                "Camera feed saved (timestamp: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ").",
                "Incident escalated to physical security team.",
            ],
            "blocks": ["USB Killer (Electrical)", "Fake USB Charging Cable (O.MG)"],
        },
        "USB Condom / Data Blocker": {
            "description": "Hardware USB data blocker that passes only power, no data lines.",
            "steps": [
                "USB Data Blocker inserted between cable and port...",
                "Power lines (VBUS, GND): CONNECTED.",
                "Data lines (D+, D-): PHYSICALLY SEVERED.",
                "Device enumeration not possible -- data transfer blocked.",
                "Charging proceeds safely -- no data exchange.",
                "All USB implant/HID attacks neutered at hardware level.",
            ],
            "blocks": ["BadUSB / HID Injection", "Rubber Ducky Script",
                       "Fake USB Charging Cable (O.MG)", "Data Exfiltration via USB"],
        },
        "Autorun Disable + AV Scan": {
            "description": "Disable autorun.inf execution and scan USB on insertion.",
            "steps": [
                "Autorun disabled via GPO: NoDriveTypeAutoRun = 0xFF...",
                "USB inserted -- autorun.inf execution prevented.",
                "Triggering on-demand antivirus scan of USB volume...",
                "AV Engine scanning 2,341 files on USB...",
                "DETECTED: Trojan.GenericKD.46234532 in setup.exe.",
                "Malware quarantined -- USB flagged as threat source.",
            ],
            "blocks": ["USB Drop / Autorun Malware"],
        },
    }

    def __init__(self):
        self.active = False

    def run_defense(self, policy_name, log_callback, status_callback, progress_callback):
        """Execute the selected defense policy."""
        policy = self.DEFENSE_POLICIES[policy_name]
        self.active = True
        steps = policy["steps"]

        status_callback(f"[+] DEFENSE ACTIVE: {policy_name}", ACCENT_BLUE)

        for i, step in enumerate(steps):
            if not self.active:
                break
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            log_callback(f"[{timestamp}] [DEFENSE] {step}", ACCENT_GRN)
            progress_callback(int((i + 1) / len(steps) * 100))
            time.sleep(random.uniform(0.5, 1.2))

        if self.active:
            log_callback(f"\n{'-'*60}", ACCENT_GRN)
            log_callback(f"[DEFENSE COMPLETE] Policy '{policy_name}' enforced.", ACCENT_GRN)
            log_callback(f"[BLOCKS ATTACKS]  {', '.join(policy['blocks'])}", ACCENT_BLUE)
            log_callback(f"{'-'*60}\n", ACCENT_GRN)
            status_callback(f"[OK]  DEFENSE SUCCEEDED -- {policy_name}", ACCENT_GRN)
        self.active = False

    def stop(self):
        self.active = False

    def check_effectiveness(self, attack_name, defense_name):
        """Returns True if the defense blocks the given attack."""
        policy = self.DEFENSE_POLICIES.get(defense_name, {})
        return attack_name in policy.get("blocks", [])


# ------------------------- Statistics Tracker -----------------------------
class SimulationStats:
    def __init__(self):
        self.attacks_launched  = 0
        self.defenses_run      = 0
        self.attacks_blocked   = 0
        self.attacks_succeeded = 0
        self.session_start     = datetime.now()

    def record_scenario(self, blocked: bool):
        self.attacks_launched  += 1
        self.defenses_run      += 1
        if blocked:
            self.attacks_blocked   += 1
        else:
            self.attacks_succeeded += 1

    def summary(self):
        elapsed = datetime.now() - self.session_start
        return {
            "Attacks Launched":   self.attacks_launched,
            "Defenses Run":       self.defenses_run,
            "Attacks Blocked":    self.attacks_blocked,
            "Attacks Succeeded":  self.attacks_succeeded,
            "Block Rate":         f"{(self.attacks_blocked / max(self.attacks_launched, 1)) * 100:.0f}%",
            "Session Duration":   str(elapsed).split(".")[0],
        }


# ----------------------------- Main GUI -----------------------------------
class USBCyberRangeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("USB Cyber Range -- Attack-Defense Simulation")
        self.root.geometry("1280x820")
        self.root.minsize(960, 700)
        self.root.configure(bg=BG_DARK)

        self.attack_engine  = USBAttackEngine()
        self.defense_engine = DeviceControlDefense()
        self.stats          = SimulationStats()

        self._build_ui()
        self._animate_banner()

    # -- UI Construction ---------------------------------------------------
    def _build_ui(self):
        self._build_header()
        self._build_main_body()
        self._build_status_bar()

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=BG_PANEL, height=72)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="[!] USB CYBER RANGE", font=("Courier New", 18, "bold"),
                 bg=BG_PANEL, fg=ACCENT_RED).pack(side="left", padx=20, pady=16)
        tk.Label(hdr, text="Attack-Defense Simulation  |  Cyber Range as a Service",
                 font=("Courier New", 10), bg=BG_PANEL, fg=TEXT_SUB).pack(side="left", padx=0, pady=22)

        # Live clock
        self.clock_var = tk.StringVar()
        tk.Label(hdr, textvariable=self.clock_var, font=("Courier New", 11),
                 bg=BG_PANEL, fg=ACCENT_BLUE).pack(side="right", padx=20)
        self._tick_clock()

    def _tick_clock(self):
        self.clock_var.set(datetime.now().strftime("[*] %Y-%m-%d  %H:%M:%S"))
        self.root.after(1000, self._tick_clock)

    def _build_main_body(self):
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=12, pady=8)

        # Left panel -- controls
        left = tk.Frame(body, bg=BG_PANEL, width=340, bd=0, highlightthickness=1,
                        highlightbackground=BORDER)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)
        self._build_left_panel(left)

        # Right panel -- log + stats
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)
        self._build_right_panel(right)

    def _build_left_panel(self, parent):
        # -- Attack Section --
        tk.Label(parent, text="[ATK]  ATTACK VECTORS", font=("Courier New", 11, "bold"),
                 bg=BG_PANEL, fg=ACCENT_RED).pack(anchor="w", padx=16, pady=(16, 4))
        tk.Frame(parent, bg=ACCENT_RED, height=1).pack(fill="x", padx=16)

        self.attack_var = tk.StringVar(value=list(USBAttackEngine.ATTACK_TYPES.keys())[0])
        for name in USBAttackEngine.ATTACK_TYPES:
            rb = tk.Radiobutton(parent, text=name, variable=self.attack_var,
                                value=name, font=("Courier New", 9),
                                bg=BG_PANEL, fg=TEXT_MAIN, selectcolor=BG_CARD,
                                activebackground=BG_PANEL, activeforeground=ACCENT_RED,
                                anchor="w", wraplength=280, justify="left",
                                command=self._on_attack_select)
            rb.pack(fill="x", padx=16, pady=2)

        # Attack info
        self.attack_info = tk.Label(parent, text="", font=("Courier New", 8),
                                    bg=BG_CARD, fg=TEXT_SUB, wraplength=290,
                                    justify="left", pady=6, padx=8)
        self.attack_info.pack(fill="x", padx=16, pady=(4, 0))

        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=16, pady=12)

        # -- Defense Section --
        tk.Label(parent, text="[DEF]  DEFENSE POLICIES", font=("Courier New", 11, "bold"),
                 bg=BG_PANEL, fg=ACCENT_BLUE).pack(anchor="w", padx=16, pady=(0, 4))
        tk.Frame(parent, bg=ACCENT_BLUE, height=1).pack(fill="x", padx=16)

        self.defense_var = tk.StringVar(value=list(DeviceControlDefense.DEFENSE_POLICIES.keys())[0])
        for name in DeviceControlDefense.DEFENSE_POLICIES:
            rb = tk.Radiobutton(parent, text=name, variable=self.defense_var,
                                value=name, font=("Courier New", 9),
                                bg=BG_PANEL, fg=TEXT_MAIN, selectcolor=BG_CARD,
                                activebackground=BG_PANEL, activeforeground=ACCENT_BLUE,
                                anchor="w", wraplength=280, justify="left",
                                command=self._on_defense_select)
            rb.pack(fill="x", padx=16, pady=2)

        # Defense info
        self.defense_info = tk.Label(parent, text="", font=("Courier New", 8),
                                     bg=BG_CARD, fg=TEXT_SUB, wraplength=290,
                                     justify="left", pady=6, padx=8)
        self.defense_info.pack(fill="x", padx=16, pady=(4, 0))

        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=16, pady=10)

        # -- Action Buttons --
        btn_frame = tk.Frame(parent, bg=BG_PANEL)
        btn_frame.pack(fill="x", padx=16, pady=4)

        self.btn_attack = tk.Button(btn_frame, text="[!]  LAUNCH ATTACK", font=("Courier New", 10, "bold"),
                                    bg=ACCENT_RED, fg="white", relief="flat", cursor="hand2",
                                    activebackground="#cc0000", activeforeground="white",
                                    command=self._run_attack_thread, padx=8, pady=8)
        self.btn_attack.pack(fill="x", pady=2)

        self.btn_defense = tk.Button(btn_frame, text="[+]  ACTIVATE DEFENSE", font=("Courier New", 10, "bold"),
                                     bg=ACCENT_BLUE, fg="white", relief="flat", cursor="hand2",
                                     activebackground="#3070bb", activeforeground="white",
                                     command=self._run_defense_thread, padx=8, pady=8)
        self.btn_defense.pack(fill="x", pady=2)

        self.btn_scenario = tk.Button(btn_frame, text="[>]  RUN FULL SCENARIO", font=("Courier New", 10, "bold"),
                                      bg=ACCENT_PUR, fg="white", relief="flat", cursor="hand2",
                                      activebackground="#8855cc", activeforeground="white",
                                      command=self._run_scenario_thread, padx=8, pady=8)
        self.btn_scenario.pack(fill="x", pady=2)

        self.btn_stop = tk.Button(btn_frame, text="[X]  STOP", font=("Courier New", 9, "bold"),
                                  bg=BG_CARD, fg=ACCENT_YEL, relief="flat", cursor="hand2",
                                  activebackground=BORDER, command=self._stop_all, padx=8, pady=6)
        self.btn_stop.pack(fill="x", pady=2)

        self.btn_clear = tk.Button(btn_frame, text="[-]  CLEAR LOG", font=("Courier New", 9),
                                   bg=BG_CARD, fg=TEXT_SUB, relief="flat", cursor="hand2",
                                   activebackground=BORDER, command=self._clear_log, padx=8, pady=6)
        self.btn_clear.pack(fill="x", pady=2)

        # Initial info load
        self._on_attack_select()
        self._on_defense_select()

    def _build_right_panel(self, parent):
        # Top: progress + status
        top = tk.Frame(parent, bg=BG_DARK)
        top.pack(fill="x", pady=(0, 6))

        self.status_var = tk.StringVar(value="[*]  SYSTEM READY -- Select an attack and defense, then run a simulation.")
        tk.Label(top, textvariable=self.status_var, font=("Courier New", 10, "bold"),
                 bg=BG_DARK, fg=ACCENT_GRN, anchor="w").pack(fill="x")

        self.progress = ttk.Progressbar(top, orient="horizontal", mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=(4, 0))
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TProgressbar", troughcolor=BG_CARD, background=ACCENT_BLUE, thickness=6)

        # Notebook: log + stats + matrix
        self.nb = ttk.Notebook(parent)
        self.nb.pack(fill="both", expand=True)
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_CARD, foreground=TEXT_SUB,
                        font=("Courier New", 9, "bold"), padding=(12, 6))
        style.map("TNotebook.Tab", background=[("selected", BG_PANEL)],
                  foreground=[("selected", ACCENT_BLUE)])

        # Tab 1 -- Event Log
        log_frame = tk.Frame(self.nb, bg=BG_DARK)
        self.nb.add(log_frame, text="  [LOG]  EVENT LOG  ")
        self.log = scrolledtext.ScrolledText(log_frame, bg=BG_DARK, fg=TEXT_MAIN,
                                             font=("Courier New", 9), insertbackground=TEXT_MAIN,
                                             bd=0, relief="flat", state="disabled",
                                             selectbackground=BG_CARD)
        self.log.pack(fill="both", expand=True)
        # Tags
        for tag, color in [("red", ACCENT_RED), ("green", ACCENT_GRN), ("blue", ACCENT_BLUE),
                            ("yellow", ACCENT_YEL), ("purple", ACCENT_PUR), ("sub", TEXT_SUB)]:
            self.log.tag_config(tag, foreground=color)

        # Tab 2 -- Stats dashboard
        stats_frame = tk.Frame(self.nb, bg=BG_PANEL)
        self.nb.add(stats_frame, text="  [STS]  STATISTICS  ")
        self._build_stats_tab(stats_frame)

        # Tab 3 -- Attack-Defense Matrix
        matrix_frame = tk.Frame(self.nb, bg=BG_PANEL)
        self.nb.add(matrix_frame, text="  [MTX]  A-D MATRIX  ")
        self._build_matrix_tab(matrix_frame)

        # Tab 4 -- About
        about_frame = tk.Frame(self.nb, bg=BG_PANEL)
        self.nb.add(about_frame, text="  [?]  ABOUT  ")
        self._build_about_tab(about_frame)

    def _build_stats_tab(self, parent):
        tk.Label(parent, text="SESSION STATISTICS", font=("Courier New", 13, "bold"),
                 bg=BG_PANEL, fg=ACCENT_BLUE).pack(pady=(20, 10))

        self.stat_labels = {}
        keys = ["Attacks Launched", "Defenses Run", "Attacks Blocked",
                 "Attacks Succeeded", "Block Rate", "Session Duration"]
        for key in keys:
            row = tk.Frame(parent, bg=BG_CARD, padx=12, pady=8)
            row.pack(fill="x", padx=40, pady=3)
            tk.Label(row, text=key, font=("Courier New", 10), bg=BG_CARD,
                     fg=TEXT_SUB, width=22, anchor="w").pack(side="left")
            lbl = tk.Label(row, text="--", font=("Courier New", 10, "bold"),
                           bg=BG_CARD, fg=TEXT_MAIN, anchor="e")
            lbl.pack(side="right")
            self.stat_labels[key] = lbl

        tk.Button(parent, text="?  REFRESH STATS", font=("Courier New", 9, "bold"),
                  bg=ACCENT_BLUE, fg="white", relief="flat", cursor="hand2",
                  command=self._refresh_stats, padx=10, pady=6).pack(pady=20)

    def _build_matrix_tab(self, parent):
        tk.Label(parent, text="ATTACK vs. DEFENSE EFFECTIVENESS MATRIX",
                 font=("Courier New", 11, "bold"), bg=BG_PANEL, fg=ACCENT_PUR).pack(pady=(16, 8))
        tk.Label(parent, text="[OK] = Defense blocks attack    [X] = Attack may succeed",
                 font=("Courier New", 8), bg=BG_PANEL, fg=TEXT_SUB).pack()

        canvas = tk.Canvas(parent, bg=BG_PANEL, highlightthickness=0)
        hscroll = ttk.Scrollbar(parent, orient="horizontal", command=canvas.xview)
        vscroll = ttk.Scrollbar(parent, orient="vertical",   command=canvas.yview)
        canvas.configure(xscrollcommand=hscroll.set, yscrollcommand=vscroll.set)
        hscroll.pack(side="bottom", fill="x")
        vscroll.pack(side="right",  fill="y")
        canvas.pack(fill="both", expand=True)

        inner = tk.Frame(canvas, bg=BG_PANEL)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        attacks  = list(USBAttackEngine.ATTACK_TYPES.keys())
        defenses = list(DeviceControlDefense.DEFENSE_POLICIES.keys())

        # Header row
        tk.Label(inner, text="Attack \\ Defense", font=("Courier New", 8, "bold"),
                 bg=BG_CARD, fg=TEXT_MAIN, width=28, anchor="w",
                 relief="flat", padx=4, pady=4).grid(row=0, column=0, padx=1, pady=1)
        for j, d in enumerate(defenses):
            tk.Label(inner, text=d[:20], font=("Courier New", 7, "bold"),
                     bg=BG_CARD, fg=ACCENT_BLUE, width=18, wraplength=100,
                     relief="flat", padx=2, pady=4).grid(row=0, column=j+1, padx=1, pady=1)

        # Data rows
        for i, a in enumerate(attacks):
            tk.Label(inner, text=a[:30], font=("Courier New", 8),
                     bg=BG_CARD, fg=TEXT_MAIN, width=28, anchor="w",
                     relief="flat", padx=4, pady=4).grid(row=i+1, column=0, padx=1, pady=1)
            for j, d in enumerate(defenses):
                blocks = self.defense_engine.check_effectiveness(a, d)
                symbol = "  [OK]" if blocks else "  [X] "
                color  = ACCENT_GRN if blocks else ACCENT_RED
                tk.Label(inner, text=symbol, font=("Courier New", 11, "bold"),
                         bg=BG_DARK, fg=color, width=4,
                         relief="flat", pady=4).grid(row=i+1, column=j+1, padx=1, pady=1)

    def _build_about_tab(self, parent):
        text = (
            "USB ATTACK SIMULATION VS DEVICE CONTROL DEFENSE\n"
            "Cyber Range as a Service -- Activity 2\n\n"
            "OVERVIEW\n"
            "This tool simulates USB-based cyber attacks and demonstrates how\n"
            "device control defense mechanisms can prevent or mitigate them.\n\n"
            "ATTACK TYPES SIMULATED\n"
            "? BadUSB / HID Injection\n"
            "? Rubber Ducky Script\n"
            "? USB Drop / Autorun Malware\n"
            "? USB Killer (Electrical)\n"
            "? Data Exfiltration via USB\n"
            "? Fake USB Charging Cable (O.MG)\n\n"
            "DEFENSE MECHANISMS\n"
            "? USB Port Blocking (OS/GPO level)\n"
            "? Device Whitelisting (VID/PID)\n"
            "? Endpoint DLP\n"
            "? Physical USB Port Guard\n"
            "? USB Data Blocker / Condom\n"
            "? Autorun Disable + AV Scan\n\n"
            "FRAMEWORKS REFERENCED\n"
            "? MITRE ATT&CK (ICS & Enterprise)\n"
            "? NIST SP 800-53 (Media Protection)\n"
            "? CIS Control 10 (Removable Media)\n\n"
            "LIBRARIES USED\n"
            "? tkinter -- GUI framework\n"
            "? threading -- concurrent simulation\n"
            "? random, time -- realistic simulation delays\n"
            "? datetime -- timestamped event logging"
        )
        st = scrolledtext.ScrolledText(parent, bg=BG_PANEL, fg=TEXT_MAIN,
                                       font=("Courier New", 10), bd=0, state="normal", wrap="word")
        st.insert("1.0", text)
        st.configure(state="disabled")
        st.pack(fill="both", expand=True, padx=20, pady=16)

    def _build_status_bar(self):
        bar = tk.Frame(self.root, bg=BG_CARD, height=26)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        tk.Label(bar, text="Cyber Range as a Service  |  USB Attack-Defense Simulation  |  Educational Purpose Only",
                 font=("Courier New", 8), bg=BG_CARD, fg=TEXT_SUB).pack(side="left", padx=10, pady=4)

    # -- Banner animation --------------------------------------------------
    def _animate_banner(self):
        msgs = [
            "[*]  SYSTEM READY -- Select an attack and defense, then run a simulation.",
            "[>]  TIP: Use Run Full Scenario to see attack vs. defense interaction.",
            "[>]  Check the A-D Matrix tab to see which defenses block which attacks.",
        ]
        self._banner_idx = 0
        self._banner_msgs = msgs

        def cycle():
            self.status_var.set(self._banner_msgs[self._banner_idx % len(self._banner_msgs)])
            self._banner_idx += 1
            self.root.after(4000, cycle)

        self.root.after(4000, cycle)

    # -- Info updates ------------------------------------------------------
    def _on_attack_select(self, *_):
        name = self.attack_var.get()
        info = USBAttackEngine.ATTACK_TYPES[name]
        sev_color = ACCENT_RED if info["severity"] == "CRITICAL" else ACCENT_YEL
        self.attack_info.configure(
            text=f"Severity: {info['severity']}\n{info['description']}\n{info['mitre']}",
            fg=sev_color)

    def _on_defense_select(self, *_):
        name = self.defense_var.get()
        info = DeviceControlDefense.DEFENSE_POLICIES[name]
        self.defense_info.configure(text=info["description"], fg=ACCENT_BLUE)

    # -- Logging -----------------------------------------------------------
    def _log(self, msg, color=TEXT_MAIN):
        tag_map = {
            ACCENT_RED: "red", ACCENT_GRN: "green", ACCENT_BLUE: "blue",
            ACCENT_YEL: "yellow", ACCENT_PUR: "purple", TEXT_SUB: "sub",
        }
        tag = tag_map.get(color, None)
        self.log.configure(state="normal")
        if tag:
            self.log.insert("end", msg + "\n", tag)
        else:
            self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _set_status(self, msg, color=ACCENT_GRN):
        self.status_var.set(msg)

    def _set_progress(self, val):
        self.progress["value"] = val

    # -- Thread runners ----------------------------------------------------
    def _run_attack_thread(self):
        name = self.attack_var.get()
        self._log(f"\n{'='*60}", ACCENT_RED)
        self._log(f"  INITIATING ATTACK: {name}", ACCENT_RED)
        self._log(f"{'='*60}", ACCENT_RED)
        t = threading.Thread(target=self.attack_engine.run_attack,
                             args=(name, self._log, self._set_status, self._set_progress),
                             daemon=True)
        t.start()

    def _run_defense_thread(self):
        name = self.defense_var.get()
        self._log(f"\n{'='*60}", ACCENT_BLUE)
        self._log(f"  ACTIVATING DEFENSE: {name}", ACCENT_BLUE)
        self._log(f"{'='*60}", ACCENT_BLUE)
        t = threading.Thread(target=self.defense_engine.run_defense,
                             args=(name, self._log, self._set_status, self._set_progress),
                             daemon=True)
        t.start()

    def _run_scenario_thread(self):
        attack_name  = self.attack_var.get()
        defense_name = self.defense_var.get()
        t = threading.Thread(target=self._scenario_worker,
                             args=(attack_name, defense_name), daemon=True)
        t.start()

    def _scenario_worker(self, attack_name, defense_name):
        """Run attack then defense, then show result."""
        self._log(f"\n{'#'*60}", ACCENT_PUR)
        self._log(f"  CYBER RANGE SCENARIO STARTING", ACCENT_PUR)
        self._log(f"  Attack  : {attack_name}", ACCENT_RED)
        self._log(f"  Defense : {defense_name}", ACCENT_BLUE)
        self._log(f"{'#'*60}\n", ACCENT_PUR)

        # Phase 1: Attack
        time.sleep(0.3)
        self.attack_engine.run_attack(attack_name, self._log, self._set_status, self._set_progress)
        time.sleep(1.0)

        # Phase 2: Defense
        self._log(f"\n{'-'*60}", ACCENT_BLUE)
        self._log("  DEFENSE SYSTEM RESPONDS...", ACCENT_BLUE)
        self._log(f"{'-'*60}\n", ACCENT_BLUE)
        self.defense_engine.run_defense(defense_name, self._log, self._set_status, self._set_progress)
        time.sleep(0.5)

        # Phase 3: Outcome
        blocked = self.defense_engine.check_effectiveness(attack_name, defense_name)
        self.stats.record_scenario(blocked)

        self._log(f"\n{'='*60}", ACCENT_PUR)
        self._log("  SCENARIO OUTCOME", ACCENT_PUR)
        if blocked:
            self._log(f"  [OK]  ATTACK BLOCKED -- Defense '{defense_name}' was EFFECTIVE.", ACCENT_GRN)
            self._set_status(f"[OK]  SCENARIO RESULT: Attack blocked by {defense_name}", ACCENT_GRN)
        else:
            self._log(f"  [!!]  ATTACK SUCCEEDED -- '{defense_name}' does NOT cover this attack vector.", ACCENT_RED)
            self._log(f"      Recommendation: Combine multiple defenses for layered security.", ACCENT_YEL)
            self._set_status(f"[!!]  SCENARIO RESULT: Defense insufficient -- attack succeeded", ACCENT_RED)
        self._log(f"{'='*60}\n", ACCENT_PUR)
        self._set_progress(100)
        self._refresh_stats()

    def _stop_all(self):
        self.attack_engine.stop()
        self.defense_engine.stop()
        self._set_status("[X]  Simulation stopped by user.", ACCENT_YEL)
        self._set_progress(0)

    def _refresh_stats(self):
        summary = self.stats.summary()
        for key, lbl in self.stat_labels.items():
            val = summary.get(key, "--")
            color = ACCENT_GRN if key == "Block Rate" else TEXT_MAIN
            if key == "Attacks Succeeded" and int(summary.get("Attacks Succeeded", 0)) > 0:
                color = ACCENT_RED
            lbl.configure(text=str(val), fg=color)


# --------------------------------- Entry ----------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app  = USBCyberRangeGUI(root)
    root.mainloop()
