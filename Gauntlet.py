``bash
cat > gauntlet.py << 'EOF'
#!/usr/bin/env python3
import argparse
import sys
import socket
import requests
from concurrent.futures import ThreadPoolExecutor

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except:
    print("Please install rich: pip install rich")
    sys.exit(1)

from payloads import SHELLS, EXPLOITS, WORDLISTS

console = Console()
VERSION = "2.0.0"

def banner():
    console.print(Panel("""
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ██████╗ ███████╗ █████╗ ██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔════╝██╔══██╗██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██████╔╝█████╗  ███████║██║  ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██╔══██╗██╔══╝  ██╔══██║██║  ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ██║  ██║███████╗██║  ██║██████╔╝
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
""", title=f"Gauntlet v{VERSION}", style="bold green", border_style="green"))

def menu():
    console.print("\n[bold cyan]Menu:[/bold cyan]")
    console.print("1. Subdomain Enumeration")
    console.print("2. Port Scan")
    console.print("3. OWASP Top 10")
    console.print("4. WAF Detection")
    console.print("5. Vulnerability Scanner")
    console.print("6. OSINT")
    console.print("7. List Payloads")
    console.print("0. Exit\n")

def validate_target(target):
    if not target:
        return False
    if target.startswith("http://") or target.startswith("https://"):
        return True
    try:
        socket.inet_aton(target)
        return True
    except:
        pass
    if "." in target:
        return True
    return False

def enumerate_subdomains(target):
    console.print(f"\n[cyan]Enumerating subdomains for: {target}[/cyan]")
    domain = target.replace("http://", "").replace("https://", "").split("/")[0]
    
    subs = WORDLISTS["subdomains"]
    found = []
    
    def check(sub):
        try:
            socket.setdefaulttimeout(2)
            socket.gethostbyname(f"{sub}.{domain}")
            return f"{sub}.{domain}"
        except:
            return None
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(check, subs)
        for result in results:
            if result:
                found.append(result)
                console.print(f"[green]+ {result}[/green]")
    
    if not found:
        console.print("[yellow]No subdomains found[/yellow]")

def scan_ports(target):
    console.print(f"\n[cyan]Scanning ports for: {target}[/cyan]")
    domain = target.replace("http://", "").replace("https://", "").split("/")[0]
    
    ports = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 80: "HTTP", 
             110: "POP3", 443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP", 8080: "Proxy"}
    
    open_ports = []
    
    def check(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            if s.connect_ex((domain, port)) == 0:
                return (port, ports.get(port, "Unknown"))
            s.close()
        except:
            pass
        return None
    
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = executor.map(check, ports.keys())
        for result in results:
            if result:
                open_ports.append(result)
                console.print(f"[green]+ Port {result[0]} ({result[1]}) - OPEN[/green]")
    
    if not open_ports:
        console.print("[yellow]No open ports found[/yellow]")

def owasp_audit(target):
    console.print(f"\n[cyan]Running OWASP Top 10 for: {target}[/cyan]")
    url = target if target.startswith("http") else f"http://{target}"
    
    paths = ["/admin", "/config", "/.git", "/backup", "/wp-admin", "/phpmyadmin"]
    found = []
    
    for path in paths:
        try:
            r = requests.get(f"{url}{path}", timeout=5)
            if r.status_code == 200:
                found.append(path)
                console.print(f"[green]+ Found: {path}[/green]")
        except:
            pass
    
    if not found:
        console.print("[yellow]No interesting paths found[/yellow]")

def waf_detection(target):
    console.print(f"\n[cyan]Detecting WAF for: {target}[/cyan]")
    url = target if target.startswith("http") else f"http://{target]"
    
    try:
        r = requests.get(f"{url}/?test=<script>", timeout=10)
        headers = " ".join(r.headers.values()).lower()
        
        if "cloudflare" in headers:
            console.print("[green]+ Cloudflare WAF detected[/green]")
        elif "akamai" in headers:
            console.print("[green]+ Akamai WAF detected[/green]")
        elif "imperva" in headers or "incapsula" in headers:
            console.print("[green]+ Imperva WAF detected[/green]")
        else:
            console.print("[yellow]No WAF detected[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def vuln_scan(target):
    console.print(f"\n[cyan]Scanning vulnerabilities for: {target}[/cyan]")
    url = target if target.startswith("http") else f"http://{target}"
    
    files = ["/.git/config", "/wp-config.php", "/.env", "/config.php", "/phpinfo.php"]
    found = []
    
    for f in files:
        try:
            r = requests.get(f"{url}{f}", timeout=5)
            if r.status_code == 200 and len(r.text) > 0:
                found.append(f)
                console.print(f"[green]+ Found: {f}[/green]")
        except:
            pass
    
    if not found:
        console.print("[yellow]No sensitive files found[/yellow]")

def osint_gather(target):
    console.print(f"\n[cyan]Gathering OSINT for: {target}[/cyan]")
    domain = target.replace("http://", "").replace("https://", "").split("/")[0]
    
    try:
        ip = socket.gethostbyname(domain)
        console.print(f"[green]+ DNS: {domain} -> {ip}[/green]")
    except:
        console.print("[red]+ DNS resolution failed[/red]")
    
    try:
        r = requests.head(f"http://{domain}", timeout=5)
        server = r.headers.get("Server", "Unknown")
        console.print(f"[green]+ Server: {server}[/green]")
    except:
        console.print("[yellow]+ Could not detect server[/yellow]")

def list_payloads():
    console.print("\n[cyan]=== Available Payloads ===[/cyan]\n")
    
    console.print("[bold]Reverse Shells:[/bold]")
    for s in SHELLS:
        console.print(f"  {s['id']}. {s['name']} ({s['os']})")
    
    console.print("\n[bold]Exploits:[/bold]")
    for e in EXPLOITS:
        console.print(f"  {e['cve']} - {e['name']} [{e['severity']}]")

def main():
    parser = argparse.ArgumentParser(description="Gauntlet Security Framework")
    parser.add_argument("-t", "--target", help="Target URL/IP")
    parser.add_argument("-v", "--version", action="store_true")
    args = parser.parse_args()
    
    if args.version:
        console.print(f"Gauntlet v{VERSION}")
        sys.exit(0)
    
    banner()
    
    if args.target:
        target = args.target
    else:
        target = input("\n[+] Enter target: ").strip()
    
    if not validate_target(target):
        console.print("[red]Invalid target![/red]")
        sys.exit(1)
    
    console.print(f"[green]Target: {target}[/green]\n")
    
    while True:
        try:
            menu()
            choice = input("[+] Select option: ").strip()
            
            if choice == "0":
                console.print("\n[green]Goodbye![/green]")
                break
            elif choice == "1":
                enumerate_subdomains(target)
            elif choice == "2":
                scan_ports(target)
            elif choice == "3":
                owasp_audit(target)
            elif choice == "4":
                waf_detection(target)
            elif choice == "5":
                vuln_scan(target)
            elif choice == "6":
                osint_gather(target)
            elif choice == "7":
                list_payloads()
            else:
                console.print("[red]Invalid option![/red]")
            
            print()
        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting...[/yellow]")
            break

if __name__ == "__main__":
    main()
