#!/usr/bin/env python3
import subprocess
import urllib.request
import json

def check_cellular_ip():
    print("================================================================")
    print("         CELLULAR INTERFACE (ccmni1) ROUTING CHECK              ")
    print("================================================================")
    
    # Your cellular IP from ifconfig was 192.0.0.4 on interface v4-ccmni1
    cellular_ip = "192.0.0.4"
    port = 11434
    
    url = f"http://{cellular_ip}:{port}/api/tags"
    print(f"[*] Testing connection to cellular interface endpoint: {url}")
    
    try:
        req = urllib.request.urlopen(url, timeout=3)
        if req.status == 200:
            print(f"[+] SUCCESS! Ollama is reachable via cellular IP {cellular_ip}")
            data = json.loads(req.read().decode())
            models = [m.get('name') for m in data.get('models', [])]
            print(f"[+] Active models: {models}")
        else:
            print(f"[!] Status code: {req.status}")
    except Exception as e:
        print(f"[!] Connection timed out or refused on cellular IP: {e}")
        print("\n[*] NOTE: On Android cellular data (carrier CGNAT/APN routing),")
        print("    external IPs like 192.0.0.4 cannot accept inbound socket loops")
        print("    from the same device. Use localhost (127.0.0.1:11434) locally.")
    print("================================================================")

if __name__ == "__main__":
    check_cellular_ip()
