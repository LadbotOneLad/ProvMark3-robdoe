#!/usr/bin/env python3
import urllib.request
import json
import os
import subprocess

OLLAMA_HOST = "http://127.0.0.1:11434"
MODEL_NAME = "gemma4:12b"

def execute_autonomous_cycle():
    print("[*] Initiating autonomous evaluation and execution cycle...")
    
    # 1. Gather deep workspace context
    files = [f for f in os.listdir(".") if f.endswith(('.py', '.json', '.sh', '.log'))]
    context = f"Node: robertu. Environment: Termux/Linux. Active files: {files}."
    
    prompt = f"""You are an autonomous systems agent running on node robertu. 
Context: {context}
Provide a single, exact bash command that can be safely run right now to verify, clean, or test the environment. 
Output ONLY the raw bash command, with no markdown code blocks, no explanations, and no extra text."""

    payload = {
        "model": MODEL_NAME,
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
        print("[*] Requesting next execution vector from local LLM...")
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode())
            command = result.get('response', '').strip().replace("```", "").strip()
            
            print(f"\n[AI DIRECTIVE COMMAND]: {command}\n")
            
            if command:
                print("[*] Executing generated directive...")
                subprocess.run(command, shell=True)
            else:
                print("[!] Received empty command stream.")
                
    except Exception as e:
        print(f"[!] Autonomous loop error: {e}")

if __name__ == "__main__":
    execute_autonomous_cycle()
