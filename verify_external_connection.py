#!/usr/bin/env python3
import urllib.request
import json

PHONE_IP = "192.168.1.101"
PORT = 11434

def test_connection():
    print("================================================================")
    print("          EXTERNAL CONNECTION VERIFICATION                      ")
    print("================================================================")
    url = f"http://{PHONE_IP}:{PORT}/api/tags"
    print(f"[*] Testing endpoint: {url}")
    
    try:
        req = urllib.request.urlopen(url, timeout=5)
        if req.status == 200:
            data = json.loads(req.read().decode())
            print(f"[+] SUCCESS! Connection established with phone Ollama node.")
            models = [m.get('name') for m in data.get('models', [])]
            print(f"[+] Available models loaded on node: {models}")
        else:
            print(f"[!] Received non-200 status: {req.status}")
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        print("[!] Ensure both devices are on the same Wi-Fi network and port 11434 is reachable.")
    print("================================================================")

if __name__ == "__main__":
    test_connection()
