#!/usr/bin/env python3
import urllib.request
import json
import subprocess

PORT = 11434
MODEL_NAME = "gemma4:12b"

def get_phone_stats():
    # Gather basic memory/process info using standard Android/Termux commands
    try:
        mem_info = subprocess.check_output(["free", "-m"], text=True)
    except Exception:
        mem_info = "N/A"
        
    try:
        top_procs = subprocess.check_output(["ps", "-e", "-o", "%cpu,%mem,cmd", "--sort=-%mem"], text=True)
        # Keep top 10 memory consumers
        top_lines = "\n".join(top_procs.splitlines()[:10])
    except Exception:
        top_lines = "N/A"
        
    return mem_info, top_lines

def analyze_and_optimize():
    print("================================================================")
    print("        OLLAMA PHONE RESOURCE & PROCESS OPTIMIZER               ")
    print("================================================================")
    
    mem, procs = get_phone_stats()
    
    prompt = f"""You are an expert mobile systems engineer optimizing a Termux/Android node.
Memory status:
{mem}

Top memory-consuming processes:
{procs}

Provide 3 precise, actionable steps or commands to free up system memory and optimize background performance on this device. Format cleanly with bullet points."""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 250, "temperature": 0.2}
    }
    
    data = json.dumps(payload).encode('utf-8')
    url = f"http://127.0.0.1:{PORT}/api/generate"
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        print(f"[*] Querying local Ollama node on port {PORT} for optimization advice...")
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode())
            advice = result.get('response', '').strip()
            
            print(f"\n[AI SYSTEM RECOMMENDATION]\n{advice}\n")
            
            with open("phone_optimization.log", "w") as log:
                log.write(advice)
            print("[+] Optimization recommendations logged to phone_optimization.log")
            
    except Exception as e:
        print(f"[!] Failed to reach Ollama node on port {PORT}: {e}")
        print("[!] Ensure the cluster is active by running fix_cluster_ports.py")
        
    print("================================================================")

if __name__ == "__main__":
    analyze_and_optimize()
