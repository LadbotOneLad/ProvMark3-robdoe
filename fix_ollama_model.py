#!/usr/bin/env python3
import urllib.request
import json

OLLAMA_HOST = "http://127.0.0.1:11434"

def get_installed_models():
    try:
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            models = [m['name'] for m in data.get('models', [])]
            return models
    except Exception as e:
        print(f"[!] Failed to fetch models: {e}")
        return []

if __name__ == "__main__":
    print("[*] Inspecting available local models...")
    models = get_installed_models()
    print(f"[+] Found models: {models}")
    
    if models:
        active_model = models[0].split(':')[0] # strip tag if needed
        print(f"[*] Updating agent_loop_exec.py to use available model: {models[0]}")
        
        with open("agent_loop_exec.py", "r") as f:
            code = f.read()
            
        # Replace MODEL_NAME line
        old_line = 'MODEL_NAME = "llama3"'
        new_line = f'MODEL_NAME = "{models[0]}"'
        
        if old_line in code:
            code = code.replace(old_line, new_line)
            with open("agent_loop_exec.py", "w") as f:
                f.write(code)
            print("[+] agent_loop_exec.py updated successfully!")
        else:
            print("[!] Could not auto-replace MODEL_NAME string, check script configuration.")
    else:
        print("[!] No local models found. Run 'ollama pull <model_name>' in your terminal first.")
