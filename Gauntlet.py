### 1. `gauntlet.py` (Main Tool)

```python
#!/usr/bin/env python3
"""
Gauntlet Security Framework - Main CLI
Author: Gauntlet Security Team
Version: 2.0.0
"""

import argparse
import sys
import os
import socket
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# Rich UI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Configuration
MODES = ["basic", "intermediate", "advanced", "pro"]
GOD_FLAG = "--GOD" in sys.argv or "--god" in sys.argv
VERSION = "2.0.0"

# Import payloads
from payloads import SHELLS, EXPLOITS, WORDLISTS

# =============================================================================
# BANNERS
# =============================================================================

def banner(mode):
    art = {
        "basic": """
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ██████╗ ███████╗ █████╗ ██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔════╝██╔══██╗██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██████╔╝█████╗  ███████║██║  ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██╔══██╗██╔══╝  ██╔══██║██║  ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ██║  ██║███████╗██║  ██║██████╔╝
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
        """,
        "god": """
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ██████╗ ███████╗ █████╗ ██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔════╝██╔══██╗██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██████╔╝█████╗  ███████║██║  ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██╔══██╗██╔══╝  ██╔══██║██║  ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ██║  ██║███████╗██║  ██║██████╔╝
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
 
                              🐉 GOD MODE 🐉
        """
    }
    colors = {"basic": "green", "god": "red bold"}
    subtitle = f"Mode: {mode.upper()}" if mode != "god" else "⚡ GOD MODE ACTIVATED ⚡"
    console.print(Panel(art.get(mode, art["basic"]), title=f"Gauntlet v{VERSION}", subtitle=subtitle, 
style=colors.get(mode, "green"), border_style=colors.get(mode, "green")))

def menu(mode):
    menus = {
        "basic": [
            ("1", "Subdomain Enumeration", "Discover subdomains"),
            ("2", "Port Scan", "Quick port scan"),
            ("3", "OWASP Top 10", "Web vulnerability"),
            ("4", "WAF Detection", "Detect WAF"),
            ("5", "Vulnerability Scanner", "Find vulns"),
            ("6", "OSINT", "Gather intel"),
            ("7", "List Payloads", "Show available payloads"),
            ("0", "Exit", "Leave Gauntlet"),
        ],
        "god": [
            ("1", "Subdomain Enumeration", "GOD MODE DNS"),
            ("2", "Port Scan", "GOD MODE SCAN"),
            ("3", "OWASP Top 10", "GOD MODE AUDIT"),
            ("4", "WAF Detection", "GOD MODE BYPASS"),
            ("5", "Vulnerability Scanner", "GOD MODE SCAN"),
            ("6", "OSINT", "GOD MODE OSINT"),
            ("7", "ALL MODULES", "RUN EVERYTHING"),
            ("8", "List Payloads", "Show payloads"),
            ("0", "Exit", "Leave Gauntlet"),
        ]
    }
    options = menus.get(mode, menus["basic"])
    table = Table(title=f"Gauntlet Menu - {mode.upper()}", show_header=True, header_style="bold cyan")
    table.add_column("#", style="cyan", width=5)
    table.add_column("Option", style="green", width=25)
    table.add_column("Description", style="white")
    for num, name, desc in options:
        table.add_row(num, name, desc)
    console.print(table)

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def validate_target(target):
    if not target:
        return False
    if target.startswith(("http://", "https://")):
        return True
    try:
        socket.inet_aton(target)
        return True
    except socket.error:
        pass
    if "." in target and len(target) < 253:
        return True
    return False

def get_target():
    while True:
        target = input("\n[+] Enter target URL/IP: ").strip()
        if validate_target(target):
            return target
        console.print("[red]Invalid target! Please enter a valid URL, IP, or domain.[/red]")

# =============================================================================
# MODULES
# =============================================================================

def enumerate_subdomains(target):
    """Subdomain Enumeration"""
    target = target.replace("http://", "").replace("https://", "").split("/")[0]
    console.print(f"\n[cyan]Enumerating subdomains for: {target}[/cyan]")
    
    # Common subdomains
    subs = ["www", "mail", "ftp", "webmail", "smtp", "pop", "ns1", "cpanel", "whm", 
            "admin", "blog", "forum", "test", "dev", "backup", "api", "cloud",
            "portal", "owa", "git", "svn", "mysql", "phpmyadmin", "autodiscover"]
    
    found = []
    
    def check_subdomain(sub):
        try:
            socket.setdefaulttimeout(2)
            socket.gethostbyname(f"{sub}.{target}")
            return f"{sub}.{target}"
        except:
            return None
    
    console.print(f"[yellow]Checking {len(subs)} subdomains...[/yellow]\n")
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(check_subdomain, subs)
        for result in results:
            if result:
                found.append(result)
                console.print(f"[green]+ Found: {result}[/green]")
    
    if found:
        table = Table(title=f"Found {len(found)} Subdomains")
        table.add_column("Subdomain", style="green")
        for sub in found:
            table.add_row(sub)
        console.print(table)
    else:
        console.print("[yellow]No subdomains found[/yellow]")
    
    return found

def scan_ports(target):
    """Port Scanning"""
    target = target.replace("http://", "").replace("https://", "").split("/")[0]
    console.print(f"\n[cyan]Scanning ports on: {target}[/cyan]")
    
    ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
        143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
        1433: "MSSQL", 1521: "Oracle", 3306: "MySQL", 3389: "RDP",
        5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 8080: "HTTP-Proxy",
        8443: "HTTPS-Alt", 27017: "MongoDB"
    }
    
    open_ports = []
    
    def check_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((target, port))
            sock.close()
            if result == 0:
                return (port, ports.get(port, "Unknown"), "Open")
        except:
            pass
        return None
    
    console.print(f"[yellow]Scanning {len(ports)} ports...[/yellow]\n")
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_port, ports.keys())
        for result in results:
            if result:
                open_ports.append(result)
                console.print(f"[green]+ Port {result[0]} ({result[1]}) - OPEN[/green]")
    
    if open_ports:
        table = Table(title=f"Open Ports ({len(open_ports)} found)")
        table.add_column("Port", style="cyan")
        table.add_column("Service", style="green")
        table.add_column("Status", style="yellow")
        for port, service, status in sorted(open_ports):
            table.add_row(str(port), service, status)
        console.print(table)
    else:
        console.print("[yellow]No open ports found[/yellow]")
    
    return open_ports

def owasp_audit(target):
    """OWASP Top 10 Audit"""
    url = target if target.startswith("http") else f"http://{target}"
    console.print(f"\n[cyan]Running OWASP Top 10 audit on: {url}[/cyan]")
    
    # Paths to check
    paths = [
        "/admin", "/admin.php", "/administrator", "/login", "/wp-admin",
        "/config", "/config.php", "/.git/config", "/.env", "/backup",
        "/phpinfo.php", "/info.php", "/server-status", "/phpmyadmin"
    ]
    
    vulns = []
    
    for path in paths:
        try:
            r = requests.get(f"{url}{path}", timeout=5, allow_redirects=False)
            if r.status_code in [200, 301, 302]:
                if "index of" not in r.text.lower():
                    vulns.append(("Interesting Path", path, f"Status: {r.status_code}"))
        except Exception as e:
            pass
    
    # Basic payloads test
    test_payloads = ["'", "\"", "<script>"]
    for payload in test_payloads:
        try:
            r = requests.get(f"{url}/?test={payload}", timeout=5)
            if any(x in r.text.lower() for x in ["sql", "error", "mysql", "syntax"]):
                vulns.append(("Possible SQL Injection", f"?test={payload}", "Potential"))
        except:
            pass
    
    if vulns:
        table = Table(title="Vulnerabilities Found")
        table.add_column("Type", style="red")
        table.add_column("Location", style="cyan")
        table.add_column("Severity", style="yellow")
        for v in vulns:
            table.add_row(v[0], v[1], v[2])
        console.print(table)
    else:
        console.print("[green]No obvious vulnerabilities detected[/green]")
    
    return vulns

def waf_detection(target):
    """WAF Detection"""
    url = target if target.startswith("http") else f"http://{target}"
    console.print(f"\n[cyan]Detecting WAF on: {url}[/cyan]")
    
    # WAF signatures
    wafs = {
        "Cloudflare": ["cf-ray", "__cfduid", "cloudflare"],
        "AWS WAF": ["awselb", "aws-waf"],
        "Akamai": ["akamai", "akamaighost"],
        "Imperva": ["incapsula", "_incapsula"],
        "Sucuri": ["sucuri", "webscan"],
        "ModSecurity": ["mod_security", "modsecurity"],
        "F5 BIG-IP": ["bigip", "ts="],
    }
    
    detected = []
    
    # Test with malicious payload
    try:
        r = requests.get(f"{url}/?q=<script>alert(1)</script>", timeout=10)
        headers = " ".join(r.headers.values()).lower()
        
        for waf_name, signatures in wafs.items():
            if any(sig in headers for sig in signatures):
                detected.append(waf_name)
        
        # Check cookies
        for cookie in r.cookies:
            if "cf" in cookie.name.lower() or "incap" in cookie.name.lower():
                detected.append("Cloudflare/Imperva")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    
    if detected:
        console.print("[green]WAF(s) Detected:[/green]")
        for waf in set(detected):
            console.print(f"  ✓ {waf}")
    else:
        console.print("[yellow]No WAF detected[/yellow]")
    
    return detected

def scan_vulns(target):
    """Vulnerability Scanner"""
    url = target if target.startswith("http") else f"http://{target}"
    console.print(f"\n[cyan]Scanning for vulnerabilities: {url}[/cyan]")
    
    # Sensitive files
    files = [
        ("/.git/config", "Git Config"),
        ("/.svn/entries", "SVN"),
        ("/wp-config.php", "WordPress Config"),
        ("/.env", "Environment File"),
        ("/config.php", "PHP Config"),
        ("/phpinfo.php", "PHP Info"),
        ("/server-info", "Apache Info"),
        ("/.DS_Store", "Mac OS X"),
        ("/backup.zip", "Backup File"),
    ]
    
    found = []
    
    for path, name in files:
        try:
            r = requests.get(f"{url}{path}", timeout=5)
            if r.status_code == 200 and len(r.text) > 0:
                found.append((name, path, "Found"))
        except:
            pass
    
    if found:
        table = Table(title="Found Files")
        table.add_column("File", style="red")
        table.add_column("Path", style="cyan")
        table.add_column("Status", style="yellow")
        for f in found:
            table.add_row(f[0], f[1], f[2])
        console.print(table)
    else:
        console.print("[green]No sensitive files found[/green]")
    
    return found

def osint_gather(target):
    """OSINT Gathering"""
    domain = target.replace("http://", "").replace("https://", "").split("/")[0]
    console.print(f"\n[cyan]Gathering OSINT for: {domain}[/cyan]")
    
    results = []
    
    # DNS Resolution
    try:
        ip = socket.gethostbyname(domain)
        results.append(("DNS Resolution", "Success", f"{domain} -> {ip}"))
    except:
        results.append(("DNS Resolution", "Failed", domain))
    
    # SSL Certificate
    try:
        import ssl
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as sock:
            sock.connect((domain, 443))
            cert = sock.getpeercert()
            subject = dict(x[0] for x in cert.get('subject', []))
            issuer = dict(x[0] for x in cert.get('issuer', []))
            results.append(("SSL Certificate", "Valid", f"Issued to: {subject.get('commonName', 'N/A')}"))
    except Exception as e:
        results.append(("SSL Certificate", "Not Available", "Port 443 closed or no SSL"))
    
    # Check HTTP headers
    try:
        r = requests.get(f"http://{domain}", timeout=5)
        server = r.headers.get('Server', 'Unknown')
        results.append(("HTTP Server", server, f"Status: {r.status_code}"))
    except:
        results.append(("HTTP Server", "Unknown", "Connection failed"))
    
    table = Table(title="OSINT Results")
    table.add_column("Category", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="white")
    for r in results:
        table.add_row(r[0], r[1], r[2])
    console.print(table)
    
    return results

def list_payloads():
    """List all available payloads"""
    console.print("\n[cyan]=== Available Payloads ===[/cyan]\n")
    
    # Reverse Shells
    table = Table(title="Reverse Shells")
    table.add_column("#", style="cyan", width=3)
    table.add_column("Name", style="green")
    table.add_column("OS", style="yellow")
    for i, shell in enumerate(SHELLS, 1):
        table.add_row(str(i), shell['name'], shell['os'])
    console.print(table)
    
    # Wordlists
    console.print("\n[cyan]Usernames:[/cyan]")
    console.print(", ".join(WORDLISTS['usernames'][:10]))
    console.print("\n[cyan]Passwords:[/cyan]")
    console.print(", ".join(WORDLISTS['passwords'][:10]))
    
    # Exploits
    console.print("\n[cyan]Exploits:[/cyan]")
    for exp in EXPLOITS:
        console.print(f"  • {exp['cve']} - {exp['name']} ({exp['severity']})")

def run_module(option, target, mode):
    """Run selected module"""
    console.print()
    
    try:
        if option == "1":
            enumerate_subdomains(target)
        elif option == "2":
            scan_ports(target)
        elif option == "3":
            owasp_audit(target)
        elif option == "4":
            waf_detection(target)
        elif option == "5":
            scan_vulns(target)
        elif option == "6":
            osint_gather(target)
        elif option == "7":
            if mode == "god":
                # Run all modules
                console.print("[bold red]🔥 RUNNING ALL MODULES IN GOD MODE 🔥[/bold red]\n")
                enumerate_subdomains(target)
                scan_ports(target)
                owasp_audit(target)
                waf_detection(target)
                scan_vulns(target)
                osint_gather(target)
            else:
                list_payloads()
        elif option == "8" and mode == "god":
            list_payloads()
        else:
            console.print("[yellow]Invalid option or not implemented[/yellow]")
    except ImportError as e:
        console.print(f"[red]Module error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Gauntlet Security Framework")
    parser.add_argument("-t", "--target", help="Target URL/IP")
    parser.add_argument("-m", "--mode", choices=MODES + ["god"], help="Operating mode")
    parser.add_argument("--god", action="store_true", help="GOD MODE")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    args = parser.parse_args()
    
    if args.version:
        console.print(f"[cyan]Gauntlet Security Framework v{VERSION}[/cyan]")
        sys.exit(0)
    
    # Determine mode
    if GOD_FLAG or args.god:
        mode = "god"
    elif args.mode:
        mode = args.mode
    else:
        mode = "basic"
    
    # Display banner
    banner(mode)
    
    # Get target
    if args.target:
        target = args.target
        if not validate_target(target):
            console.print("[red]Invalid target provided![/red]")
            sys.exit(1)
    else:
        target = get_target()
    
    console.print(f"[green]✓ Target set to: {target}[/green]")
    console.print(f"[yellow]Mode: {mode.upper()}[/yellow]\n")
    
    # Main loop
    while True:
        try:
            menu(mode)
            sel = input("\n[+] Select option: ").strip()
            
            if sel == "0":
                console.print("\n[bold green]Thanks for using Gauntlet! Stay safe.[/bold green]")
                break
            
            # Validate option
            max_opts = 8 if mode == "god" else 7
            if not sel.isdigit() or int(sel) < 0 or int(sel) > max_opts:
                console.print("[red]Invalid option![/red]")
                continue
            
            # Run module
            run_module(sel, target, mode)
            
            # Ask to continue
            console.print()
            cont = input("[?] Continue? (Y/n): ").strip().lower()
            if cont in ["n", "no"]:
                break
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted! Exiting...[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            continue
    
    console.print("[red]Exiting Gauntlet.[/red]")
    sys.exit(0)

if __name__ == "__main__":
    main()
```
