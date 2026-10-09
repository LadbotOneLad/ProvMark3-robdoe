#!/usr/bin/env python3
import urllib.request
import json
import time

OLLAMA_HOST = "http://127.0.0.1:11434"
MODEL_NAME = "gemma4:12b"

# Standardized agent evaluation test suite (inspired by multi-step reasoning & coding benchmarks)
BENCHMARK_PROMPTS = [
    {
        "category": "Algorithmic Reasoning",
        "prompt": "Write a Python function to find the longest palindromic substring in a given string efficiently. Output only clean code inside markdown."
    },
    {
        "category": "System Architecture",
        "prompt": "Explain in 3 concise bullet points how to structure a fault-tolerant decentralized key-value store."
    },
    {
        "category": "Security & Logic",
        "prompt": "Identify the critical flaw in executing untrusted code via dynamic shell evaluation and provide the secure alternative in one sentence."
    }
]

def run_benchmark():
    print(f"================================================================")
    print(f"       AI AGENT STANDARDIZED BENCHMARK // MODEL: {MODEL_NAME}      ")
    print(f"================================================================")

    for i, test in enumerate(BENCHMARK_PROMPTS, 1):
        print(f"\n[Test {i}/3] Category: {test['category']}")
        print(f"Prompt: {test['prompt']}")
        
        payload = {
            "model": MODEL_NAME,
            "prompt": test['prompt'],
            "stream": False,
            "options": {
                "num_predict": 300,
                "temperature": 0.2
            }
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{OLLAMA_HOST}/api/generate",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        start_time = time.time()
        try:
            print("[*] Evaluating...")
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode())
                duration = time.time() - start_time
                response_text = result.get('response', '').strip()
                
                print(f"[+] Completed in {duration:.2f}s")
                print(f"--- Response ---\n{response_text}\n----------------")
                
                # Log benchmark result
                with open("benchmark_results.log", "a") as log:
                    log.write(f"Test {i} [{test['category']}] - Time: {duration:.2f}s\n{response_text}\n\n")
                    
        except Exception as e:
            print(f"[!] Test failed or timed out: {e}")

if __name__ == "__main__":
    run_benchmark()
