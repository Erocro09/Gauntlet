#!/bin/bash
echo "[*] Installing Gauntlet..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
mkdir -p payloads/upstream payloads/creds payloads/flat
cd payloads/upstream
git clone https://github.com/danielmiessler/SecLists.git || true
git clone https://github.com/swisskyrepo/PayloadsAllTheThings.git || true
git clone https://github.com/foospidy/Offensive-Payloads.git || true
git clone https://github.com/fuzzdb-project/fuzzdb.git || true
cd ../../
echo "[*] Downloading rockyou.txt..."
curl -L https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -o payloads/creds/rockyou.txt
echo "[*] Setup complete."