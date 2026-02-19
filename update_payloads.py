```python
#!/usr/bin/env python3
"""
Gauntlet Payload Update Tool
View, add, and manage payloads
"""

import json
import os
from payloads import SHELLS, EXPLOITS, WORDLISTS, WEB_PAYLOADS, get_shell, get_all_shells

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║              Gauntlet Payload Manager v2.0                    ║
╚═══════════════════════════════════════════════════════════════╝
    """)

def list_shells():
    print("\n[=== REVERSE SHELLS ===]\n")
    print(f"{'ID':<5} {'Name':<20} {'OS':<10} Payload")
    print("-" * 80)
    for shell in SHELLS:
        print(f"{shell['id']:<5} {shell['name']:<20} {shell['os']:<10} {shell['payload'][:40]}...")

def list_exploits():
    print("\n[=== EXPLOITS ===]\n")
    print(f"{'CVE':<15} {'Name':<25} {'Severity':<10} Platform")
    print("-" * 80)
    for exp in EXPLOITS:
        print(f"{exp['cve']:<15} {exp['name']:<25} {exp['severity']:<10} {exp['platform']}")

def list_wordlists():
    print("\n[=== WORDLISTS ===]\n")
    print(f"[Usernames] ({len(WORDLISTS['usernames'])}):")
    print(", ".join(WORDLISTS['usernames']))
    print(f"\n[Passwords] ({len(WORDLISTS['passwords'])}):")
    print(", ".join(WORDLISTS['passwords']))
    print(f"\n[Paths] ({len(WORDLISTS['paths'])}):")
    print(", ".join(WORDLISTS['paths']))

def list_web_payloads():
    print("\n[=== WEB PAYLOADS ===]\n")
    for category, payloads in WEB_PAYLOADS.items():
        print(f"[{category.upper()}]")
        for p in payloads[:5]:
            print(f"  - {p}")
        if len(payloads) > 5:
            print(f"  ... and {len(payloads)-5} more")
        print()

def generate_shell():
    print("\n[=== GENERATE SHELL ===]\n")
    print("Available shells:")
    for shell in SHELLS:
        print(f"  {shell['id']}. {shell['name']} ({shell['os']})")
    
    try:
        choice = int(input("\nSelect shell (0 to cancel): "))
        if choice == 0:
            return
        
        shell = get_shell(choice)
        if not shell:
            print("[!] Invalid selection")
            return
        
        # Get LHOST and LPORT
        lhost = input("LHOST (your IP): ").strip()
        lport = input("LPORT (your port): ").strip()
        
        # Generate payload
        payload = shell['payload']
        payload = payload.replace("{LHOST}", lhost).replace("{LPORT}", lport)
        
        print(f"\n[Generated Payload for {shell['name']}]:\n")
        print(payload)
        print()
        
        # Save to file
        save = input("Save to file? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"shell_{shell['name'].lower().replace(' ', '_')}.txt"
            with open(filename, 'w') as f:
                f.write(payload)
            print(f"[+] Saved to: {filename}")
        
    except ValueError:
        print("[!] Invalid input")

def main():
    while True:
        print_banner()
        print("1. List Reverse Shells")
        print("2. List Exploits")
        print("3. List Wordlists")
        print("4. List Web Payloads")
        print("5. Generate Shell")
        print("0. Exit")
        
        choice = input("\nSelect: ").strip()
        
        if choice == "1":
            list_shells()
        elif choice == "2":
            list_exploits()
        elif choice == "3":
            list_wordlists()
        elif choice == "4":
            list_web_payloads()
        elif choice == "5":
            generate_shell()
        elif choice == "0":
            print("\n[!] Exiting...")
            break
        else:
            print("[!] Invalid choice")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
```

---

### 7. `.gitignore`

```
__pycache__/
*.py[cod]
*.pyc
*.so
.Python
build/
dist/
*.egg-info/
venv/
env/
.venv/
.vscode/
.idea/
*.swp
*.log
*.db
.env
.DS_Store
*.txt
```

---
