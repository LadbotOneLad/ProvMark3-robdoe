#!/usr/bin/env python3
import urllib.request
import json
import sys

OLLAMA_HOST = "http://127.0.0.1:11434"

def check_ollama_health():
    """Check if local Ollama service is reachable."""
    try:
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags")
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                models = [m['name'] for m in data.get('models', [])]
                print(f"[+] Ollama online. Available models: {models}")
                return True
    except Exception as e:
        print(f"[!] Ollama connection failed: {e}")
        return false

def query_local_model(model_name, prompt):
    """Send a prompt directly to the local Ollama instance."""
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/generate",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result.get('response', '')
    except Exception as e:
        return f"Error querying model: {e}"

if __name__ == "__main__":
    if check_ollama_health():
        if len(sys.argv) > 2:
            model = sys.argv[1]
            prompt = sys.argv[2]
            print(f"\n[*] Querying {model}...")
            print(query_local_model(model, prompt))
        else:
            print("[*] Usage: python3 ollama_bridge_core.py <model_name> \"Your prompt here\"")
