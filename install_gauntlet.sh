
```bash
cat > install_gauntlet.sh << 'EOF'
#!/bin/bash
echo "Installing Gauntlet..."
pip3 install rich requests urllib3
chmod +x gauntlet.py
echo "Done! Run: python3 gauntlet.py"
