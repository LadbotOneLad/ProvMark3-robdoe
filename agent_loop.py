#!/usr/bin/env python3
import urllib.request
import json
import os

OLLAMA_HOST = "http://127.0.0.1:11434"
MODEL_NAME = "llama3"  # Adjust to whatever local model you have pulled

def evaluate_workspace():
    # Gather basic local state context
    files = os.listdir(".")
    context = f"Current directory files: {files}. Node ID: robertu."
    
    prompt = f"Analyze this workspace context: {context}. Give me one concise, highly technical engineering task to run next."
    
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
        print("[*] Querying local AI agent for next-step evaluation...")
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            response_text = result.get('response', '').strip()
            
            print(f"\n[AI AGENT DIRECTIVE]\n{response_text}\n")
            
            # Log decision
            with open("agent_decisions.log", "a") as log:
                log.write(f"--- Directive ---\n{response_text}\n\n")
                
    except Exception as e:
        print(f"[!] Failed to reach local AI engine: {e}")

if __name__ == "__main__":
    evaluate_workspace()
