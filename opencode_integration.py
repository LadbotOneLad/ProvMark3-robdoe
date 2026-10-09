#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess

def execute_opencode_sync():
    print("================================================================")
    print("  OPENCODE ENVIRONMENT SYNCHRONIZATION & EXECUTION              ")
    print("================================================================")
    
    for lock_path in [".git/index.lock", ".git/gc.pid"]:
        if os.path.exists(lock_path):
            os.remove(lock_path)
            
    subprocess.run(["git", "gc", "--prune=all", "--aggressive"], capture_output=True)

    opencode_payload = {
        "conductor": "Eric The Viking (PHILL)",
        "architect": "robdoe",
        "genesis": "e14f9a8d",
        "doctrine": "Opencode Native Environment Integration",
        "etherscan_tx": "D52I6WMPM4A2QW62PATAN5JS9YN962SA71",
        "harmonic_constants": {
            "arcsec_total": 1296000,
            "divisor": 3600,
            "seconds_day": 86400,
            "hours_day": 24,
            "reciprocal_scale": 1 / 7200,
            "harmonic_ratio": 0.052
        },
        "stack_depth": 216,
        "piano_keys": 88,
        "runtime_environment": "opencode"
    }
    
    hasher = hashlib.sha3_512()
    hasher.update(json.dumps(opencode_payload, sort_keys=True).encode('utf-8'))
    super_root = hasher.hexdigest()
    opencode_payload["opencode_super_root"] = super_root
    
    filename = "opencode_proof.json"
    with open(filename, "w") as f:
        json.dump(opencode_payload, f, indent=4)
        
    print(f"[+] Opencode Super-Root Locked: {super_root[:32]}...")
    
    subprocess.run(["git", "add", "-f", filename], check=True)
    subprocess.run(["git", "commit", "-m", f"opencode(sync): unified execution super-root {super_root[:16]}..."], check=True)
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    
    tags = [
        "v2026.8.11-opencode-pre-0.052",
        "v2026.8.11-opencode-omega-0.052",
        "v2026.8.11-opencode-post-0.052"
    ]
    
    for tag in tags:
        print(f"[*] Applying Opencode witness tag: {tag}")
        subprocess.run(["git", "tag", "-f", tag, "-m", f"Opencode runtime lock {tag}"], check=True)
        
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
    subprocess.run(["git", "push", "origin", "--tags", "--force"], check=True)
    
    print("[+] SUCCESS! Opencode pipeline fully synchronized, committed, tagged, and pushed upstream.")
    print("================================================================")

if __name__ == "__main__":
    execute_opencode_sync()
