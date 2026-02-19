```markdown
# Gauntlet Security Framework

<p align="center">
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ██████╗ ███████╗ █████╗ ██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔════╝██╔══██╗██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██████╔╝█████╗  ███████║██║  ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██╔══██╗██╔══╝  ██╔══██║██║  ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ██║  ██║███████╗██║  ██║██████╔╝
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
</p>

## Overview

Gauntlet is a comprehensive offensive security framework designed for penetration testers and security 
researchers.

## Features

- Subdomain Enumeration
- Port Scanning
- OWASP Top 10 Auditing
- WAF Detection
- Vulnerability Scanner
- OSINT Gathering
- Multiple Operation Modes (Basic, Advanced, GOD)

## Installation

### Quick Install (Linux/macOS)

```bash
chmod +x install_gauntlet.sh
./install_gauntlet.sh
```

### Manual Install

```bash
pip install -r requirements.txt
python3 gauntlet.py
```

## Usage

```bash
# Interactive mode
python3 gauntlet.py

# Specify target
python3 gauntlet.py -t target.com

# Specify mode
python3 gauntlet.py -m advanced

# GOD MODE
python3 gauntlet.py --god
```

## Menu Options

| # | Module | Description |
|---|--------|-------------|
| 1 | Subdomain Enumeration | Discover subdomains |
| 2 | Port Scan | Scan ports |
| 3 | OWASP Top 10 | Web vulnerability audit |
| 4 | WAF Detection | Detect WAF |
| 5 | Vulnerability Scanner | Find vulnerabilities |
| 6 | OSINT | Gather intelligence |
| 7 | List Payloads | Show available payloads |

## Requirements

- Python 3.8+
- Rich library
- Requests library

## Disclaimer

This tool is for authorized security testing only. Misuse is prohibited.

## License

MIT License - See LICENSE file
```
