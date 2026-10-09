#!/usr/bin/env python3
import subprocess
import time
import urllib.request
import json

def fix_and_verify():
    print("================================================================")
    print("         REBINDING OLLAMA TO ALL INTERFACES (0.0.0.0)           ")
    print("================================================================")
    
    # 1. Kill any existing ollama processes
    subprocess.run(["pkill", "-f", "ollama"], stderr=subprocess.DEVNULL)
    time.sleep(1)
    
    # 2. Start ollama explicitly bound to 0.0.0.0:11434 in background
    print("[*] Launching Ollama bound to 0.0.0.0:11434...")
    cmd = "OLLAMA_HOST=0.0.0.0:11434 nohup ollama serve > ollama_server.log 2>&1 &"
    subprocess.run(cmd, shell=True)
    
    print("[*] Waiting 5 seconds for server initialization...")
    time.sleep(5)
    
    # 3. Test local loopback and Wi-Fi IP
    endpoints = [
        "http://127.0.0.1:11434/api/tags",
        "http://192.168.1.101:11434/api/tags"
    ]
    
    for url in endpoints:
        print(f"[*] Testing connection to: {url}")
        try:
            req = urllib.request.urlopen(url, timeout=3)
            if req.status == 200:
                print(f"[+] SUCCESS! {url} is responding.")
            else:
                print(f"[!] {url} returned status {req.status}")
        except Exception as e:
            print(f"[!] Failed to reach {url}: {e}")
            
    print("================================================================")

if __name__ == "__main__":
    fix_and_verify()
