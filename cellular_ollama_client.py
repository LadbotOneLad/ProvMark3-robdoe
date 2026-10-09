#!/usr/bin/env python3
import urllib.request
import json

CELLULAR_IP = "192.0.0.4"
PORT = 11434
MODEL = "gemma4:12b"

def query_cellular_node(prompt_text):
    print("================================================================")
    print("        CELLULAR MESH NODE OLLAMA DISPATCHER                    ")
    print("================================================================")
    
    url = f"http://{CELLULAR_IP}:{PORT}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt_text,
        "stream": False,
        "options": {"num_predict": 150, "temperature": 0.3}
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        print(f"[*] Dispatched request to cellular interface node ({CELLULAR_IP}:{PORT})...")
        with urllib.request.urlopen(req, timeout=45) as resp:
            result = json.loads(resp.read().decode())
            response = result.get('response', '').strip()
            print(f"\n[NODE RESPONSE]\n{response}\n")
    except Exception as e:
        print(f"[!] Request failed: {e}")
        
    print("================================================================")

if __name__ == "__main__":
    query_cellular_node("Confirm active link state and node synchronization in 3 concise words.")
