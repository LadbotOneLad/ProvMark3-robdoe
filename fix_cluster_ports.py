#!/usr/bin/env python3
import subprocess
import time
import urllib.request

def restart_cluster():
    print("================================================================")
    print("          RE-SPAWNING CLUSTER DAEMONS (BACKGROUND)              ")
    print("================================================================")
    
    # Kill any dangling ollama processes
    subprocess.run(["pkill", "-f", "ollama"], stderr=subprocess.DEVNULL)
    time.sleep(1)
    
    # Launch instances with proper nohup / background detachment
    for port in [11434, 11435, 11436]:
        cmd = f"OLLAMA_HOST=0.0.0.0:{port} nohup ollama serve > ollama_{port}.log 2>&1 &"
        subprocess.run(cmd, shell=True)
        print(f"[*] Launched Ollama on port {port}")
        
    print("[*] Waiting 5 seconds for daemons to initialize sockets...")
    time.sleep(5)
    
    # Verify ports
    for port in [11434, 11435, 11436]:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/api/tags", timeout=2)
            print(f"[+] Port {port} is active and responding!")
        except Exception:
            print(f"[!] Port {port} failed health check.")
    print("================================================================")

if __name__ == "__main__":
    restart_cluster()
