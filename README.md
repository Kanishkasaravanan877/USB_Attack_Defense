# USB Attack Simulation vs Device Control Defense
## Activity 2 – Cyber Range as a Service 

A GUI-based Python simulation of USB-based cyber attacks and device control defense mechanisms, built as part of an Attack-Defense Cyber Range exercise.

---

## Overview

This tool simulates **6 real-world USB attack vectors** and **6 device control defense mechanisms** in an interactive Tkinter GUI. It demonstrates how USB threats operate at the technical level, and how corresponding defenses can detect, block, or mitigate them — all within a safe, educational simulation environment.

---

## Features

- **6 USB Attack Simulations**
  - BadUSB / HID Injection
  - Rubber Ducky Script
  - USB Drop / Autorun Malware
  - USB Killer (Electrical)
  - Data Exfiltration via USB
  - Fake USB Charging Cable (O.MG)

- **6 Defense Policy Simulations**
  - USB Port Blocking (OS/GPO)
  - Device Whitelisting (VID/PID)
  - Endpoint DLP
  - Physical USB Port Guard
  - USB Data Blocker / USB Condom
  - Autorun Disable + AV Scan

- **Real-time Event Log** with timestamped simulation output
- **Attack-Defense Matrix** — visual effectiveness grid
- **Session Statistics** — block rate, scenarios run
- **Full Scenario Mode** — attack + defense + outcome evaluation
- MITRE ATT&CK technique references per attack

---

## Requirements

- Python 3.8+
- Tkinter (built into Python on Windows/macOS; `sudo apt install python3-tk` on Linux)
- **No third-party packages required**

---

## How to Run

```bash
python usb_attack_defense.py
```

---

## File Structure

```
.
├── usb_attack_defense.py   # Main application (GUI + simulation engine)
├── README.md               # This file
└── USB_CyberRange_Report.docx  # Activity report
```

---

## Frameworks Referenced

| Framework | Relevance |
|-----------|-----------|
| MITRE ATT&CK | Attack technique mapping (T1200, T1091, T1052.001, etc.) |
| NIST SP 800-53 | Defense control alignment (MP-7, SI-3, AC-19) |
| CIS Controls v8 | Control 10 (Malware Defenses), Control 3 (Data Protection) |

---

## Disclaimer

This project is developed **strictly for educational purposes** as part of a cybersecurity coursework activity. All simulations are purely software-based and do not execute any real attacks on any system.
