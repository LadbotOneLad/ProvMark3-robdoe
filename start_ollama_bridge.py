#!/usr/bin/env python3
import subprocess
import urllib.request
import time
import sys

OLLAMA_HOST = "http://127.0.0.1:11434"

def check_connection():
    try:
        urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=2)
        return True
    except Exception:
        return False

def main():
    print("[*] Checking local Ollama service status...")
    if check_connection():
        print("[+] Ollama is already active and responding.")
        return

    print("[!] Connection refused. Attempting to start Ollama locally...")
    try:
        # Start ollama serve in the background
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for service to spin up
        for attempt in range(10):
            print(f"    -> Waiting for service response (Attempt {attempt + 1}/10)...")
            time.sleep(2)
            if check_connection():
                print("[+] Ollama server successfully online!")
                return
                
        print("[!] Timed out waiting for Ollama to start. Ensure ollama is installed and run 'ollama serve' manually.")
    except FileNotFoundError:
        print("[!] 'ollama' binary not found in PATH. Install Ollama or run it from your host/Termux environment.")

if __name__ == "__main__":
    main()
