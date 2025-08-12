#!/usr/bin/env python3
import os, subprocess

repos = [
    "SecLists",
    "PayloadsAllTheThings",
    "Offensive-Payloads",
    "fuzzdb"
]

for repo in repos:
    path = os.path.join("payloads/upstream", repo)
    if os.path.exists(path):
        print(f"[*] Updating {repo}...")
        subprocess.call(["git", "-C", path, "pull", "--rebase"])
    else:
        print(f"[*] Cloning {repo}...")
        subprocess.call(["git", "clone", f"https://github.com/{'danielmiessler/SecLists' if repo=='SecLists' else 'swisskyrepo/PayloadsAllTheThings' if repo=='PayloadsAllTheThings' else 'foospidy/Offensive-Payloads' if repo=='Offensive-Payloads' else 'fuzzdb-project/fuzzdb'}.git", path])