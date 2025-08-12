# ðŸ›¡ï¸ Gauntlet â€” Offensive Security Framework  
**Developed by Ero09**  

Gauntlet is a **multi-mode offensive security tool** built for real-world penetration testing and red team operations.  
It integrates enumeration, exploitation, cracking, and bypass techniques into one seamless CLI interface â€” optimized for both beginners and seasoned operators.  

---

## ðŸš€ Features
- **Modes**:
  - **Basic** â€“ Lightweight scan for common issues
  - **Intermediate** â€“ Deeper enumeration & vulnerability checks
  - **Advanced** â€“ Intrusive tests, async scanning, extended payloads
  - **Pro** â€“ Full arsenal with exploit modules, cracking, and bypass
  - **God** â€“ Hidden mode, no rate limits, everything unlocked (`--GOD` flag)

- **Modules**:
  - Subdomain enumeration (assetfinder, amass-like)
  - Port scanning (Nmap via python-nmap)
  - OWASP Top 10 audit
  - WAF detection & bypass
  - Bruteforce & cracking
  - DDoS feasibility checks
  - Exploit triggers (manual run)
  - Payload obfuscation & WAF evasion

- **Payload Arsenal**:
  - SecLists  
  - PayloadsAllTheThings  
  - FuzzDB  
  - Offensive-Payloads  
  - Custom bypass lists & 0day patterns

- **Compatibility**:
  - Runs on **Linux**, **Termux**, and cloud shells
  - Works offline after setup â€” payloads bundled locally

---

## ðŸ“¦ Installation
```bash
git clone https://github.com/<your-username>/Gauntlet.git
cd Gauntlet
chmod +x install_gauntlet.sh
./install_gauntlet.sh
```

---

## ðŸ•¹ï¸ Usage
```bash
python3 Gauntlet.py
```

**God Mode** (hidden):
```bash
python3 Gauntlet.py --GOD
```

---

## ðŸ“œ Example Commands
```bash
# Basic scan
python3 Gauntlet.py

# Advanced scan on example.com
python3 Gauntlet.py --mode advanced --target example.com

# God mode, full arsenal
python3 Gauntlet.py --GOD --target example.com
```

---

## âš ï¸ Disclaimer
This tool is for **authorized security testing only**.  
You are responsible for ensuring you have permission before running Gauntlet on any target.

---

### ðŸ’» Developed by: **Ero09**
> *"When the gauntlet drops, no vuln hides."*
