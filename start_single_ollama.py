#!/usr/bin/env python3
import subprocess
import time
import urllib.request
import json

def start_and_query():
    print("================================================================")
    print("        SINGLE-PORT OLLAMA HARDWARE DIAGNOSTIC LAUNCHER         ")
    print("================================================================")
    
    # 1. Terminate any existing ollama
    subprocess.run(["pkill", "-f", "ollama"], stderr=subprocess.DEVNULL)
    time.sleep(1)
    
    # 2. Start single instance on 11434 foreground/background check
    print("[*] Starting Ollama server on port 11434...")
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Wait for readiness
    print("[*] Waiting for server socket initialization...")
    for i in range(10):
        time.sleep(2)
        try:
            req = urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2)
            if req.status == 200:
                print(f"[+] Ollama server online (Attempt {i+1})!")
                break
        except Exception:
            print(f"    -> Waiting... ({i+1}/10)")
    else:
        print("[!] Failed to start Ollama server.")
        return

    # 4. Gather precise CPU, memory, and system diagnostics
    print("[*] Gathering system hardware stats (CPU, RAM, load)...")
    try:
        cpu_info = subprocess.check_output(["lscpu"], text=True)
    except Exception:
        cpu_info = "N/A"
        
    try:
        free_info = subprocess.check_output(["free", "-h"], text=True)
    except Exception:
        free_info = "N/A"
        
    try:
        top_procs = subprocess.check_output(["ps", "aux"], text=True)
        top_summary = "\n".join([line for line in top_procs.splitlines() if "ollama" in line or "python" in line or "sh" in line][:15])
    except Exception:
        top_summary = "N/A"

    prompt = f"""Analyze the following local hardware & resource state for this Android/Termux device and provide direct, optimized commands and steps to manage CPU and RAM efficiently:

=== CPU INFO ===
{cpu_info[:600]}

=== MEMORY (RAM) ===
{free_info}

=== RELEVANT PROCESSES ===
{top_summary}

Provide a concise breakdown of current resource pressure and 3 specific actionable shell commands to optimize CPU and RAM utilization."""

    payload = {
        "model": "gemma4:12b",
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 300, "temperature": 0.2}
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    print("[*] Querying Gemma model for hardware optimization strategy...")
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode())
            response_text = result.get('response', '').strip()
            print(f"\n[HARDWARE OPTIMIZATION ANALYSIS]\n{response_text}\n")
    except Exception as e:
        print(f"[!] Inference request failed: {e}")
        
    print("================================================================")

if __name__ == "__main__":
    start_and_query()
