import os
import time
import json

def gather_telemetry():
    print("[*] Gathering local node telemetry...")
    
    # Basic system info available via standard library
    telemetry = {
        "node_id": "robertu",
        "working_directory": os.getcwd(),
        "cpu_count": os.cpu_count(),
        "load_avg": os.getloadavg() if hasattr(os, "getloadavg") else "N/A",
        "timestamp": time.time()
    }
    
    output_path = "node_telemetry.json"
    with open(output_path, "w") as f:
        json.dump(telemetry, f, indent=4)
        
    print(f"[+] Telemetry captured and saved to {output_path}")

if __name__ == "__main__":
    gather_telemetry()
