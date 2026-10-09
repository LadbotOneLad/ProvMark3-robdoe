#!/usr/bin/env python3
import urllib.request
import json
import time

PORTS = [11434, 11435, 11436]
MODEL_NAME = "gemma4:12b"

def query_cluster(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 100}
    }
    data = json.dumps(payload).encode('utf-8')
    
    for port in PORTS:
        url = f"http://127.0.0.1:{port}/api/generate"
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        try:
            print(f"[*] Dispatched request to cluster node on port {port}...")
            start = time.time()
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                duration = time.time() - start
                print(f"[+] Node {port} responded successfully in {duration:.2f}s")
                return result.get('response', '').strip()
        except Exception as e:
            print(f"[!] Node {port} failed or busy: {e}. Trying next...")
            
    print("[!] All cluster nodes exhausted.")
    return None

if __name__ == "__main__":
    print("================================================================")
    print("          OLLAMA MULTI-PORT CLUSTER DISPATCHER                  ")
    print("================================================================")
    answer = query_cluster("Verify system sync state in 5 words.")
    print(f"\n[CLUSTER CONSENSUS OUTPUT]\n{answer}\n")
    print("================================================================")
