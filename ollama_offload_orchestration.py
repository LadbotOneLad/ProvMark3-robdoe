#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
import urllib.request

def query_ollama(prompt_text):
    print("[*] Offloading cognitive strain to local Ollama instance...")
    url = "http://localhost:11434/api/generate"
    data = json.dumps({
        "model": "llama3",
        "prompt": prompt_text,
        "stream": False
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            return res_json.get("response", "Ollama resonance acknowledged.")
    except Exception as e:
        return f"Ollama offline/fallback engaged: {str(e)}"

def execute_ollama_transition():
    print("================================================================")
    print("  OLLAMA COGNITIVE OFFLINK & GRAND PUSH TRANSITION             ")
    print("================================================================")
    
    ai_response = query_ollama("Verify the harmonic synchronization of the 88-key piano and Etherscan anchor D52I6WMPM4A2QW62PATAN5JS9YN962SA71 at 0.052 ratio.")
    print(f"[Ollama says]: {ai_response.strip()}")

    for lock_path in [".git/index.lock", ".git/gc.pid"]:
        if os.path.exists(lock_path):
            os.remove(lock_path)
            
    subprocess.run(["git", "gc", "--prune=all", "--aggressive"], capture_output=True)

    payload = {
        "conductor": "Eric The Viking (PHILL)",
        "architect": "robdoe",
        "genesis": "e14f9a8d",
        "doctrine": "Ollama Offloaded Cognitive Grand Transition",
        "etherscan_tx": "D52I6WMPM4A2QW62PATAN5JS9YN962SA71",
        "ollama_resonance": ai_response,
        "harmonic_constants": {
            "arcsec_total": 1296000,
            "divisor": 3600,
            "seconds_day": 86400,
            "hours_day": 24,
            "reciprocal_scale": 1 / 7200,
            "harmonic_ratio": 0.052
        },
        "stack_depth": 216,
        "piano_keys": 88
    }
    
    hasher = hashlib.sha3_512()
    hasher.update(json.dumps(payload, sort_keys=True).encode('utf-8'))
    super_root = hasher.hexdigest()
    payload["super_root"] = super_root
    
    filename = "ollama_transition_proof.json"
    with open(filename, "w") as f:
        json.dump(payload, f, indent=4)
        
    print(f"[+] Offloaded Super-Root: {super_root[:32]}...")
    
    subprocess.run(["git", "add", "-f", filename], check=True)
    subprocess.run(["git", "commit", "-m", f"ollama(transition): cognitive offload super-root {super_root[:16]}..."], check=True)
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    
    tags = [
        "v2026.8.11-ollama-pre-0.052",
        "v2026.8.11-ollama-transition-omega-0.052",
        "v2026.8.11-ollama-post-0.052"
    ]
    
    for tag in tags:
        print(f"[*] Stacking tag: {tag}")
        subprocess.run(["git", "tag", "-f", tag, "-m", f"Ollama offload witness lock {tag}"], check=True)
        
    print("[*] Executing master push upstream...")
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
    subprocess.run(["git", "push", "origin", "--tags", "--force"], check=True)
    
    print("[+] SUCCESS! Cognitive strain relieved via Ollama, fully pushed and tagged.")
    print("================================================================")

if __name__ == "__main__":
    execute_ollama_transition()
