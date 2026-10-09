import urllib.request
import json

# Target your specific network node IP
OLLAMA_URL = "http://192.0.0.4:11434/api/generate"

data = {
    "model": "llama3.2",
    "prompt": "State the current phase-lock vector status of the orchardappletree ecosystem matrix.",
    "stream": False
}

req = urllib.request.Request(
    OLLAMA_URL,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    print(f"[+] Connecting to Ollama Node at {OLLAMA_URL}...")
    with urllib.request.urlopen(req, timeout=5) as response:
        res = json.loads(response.read().decode('utf-8'))
        print("[+] Ollama Response Received:")
        print(res.get("response", "No response content."))
except Exception as e:
    print(f"[-] Connection Error to {OLLAMA_URL} -> {e}")
