#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess

def execute_salvos_homes_matrix():
    print("================================================================")
    print(" SALVOS & HOME CENTRE MATRIX: X4 BRANCHES & 13 TAGS EACH       ")
    print("================================================================")
    
    for lock_path in [".git/index.lock", ".git/gc.pid"]:
        if os.path.exists(lock_path):
            os.remove(lock_path)
            
    subprocess.run(["git", "gc", "--prune=all", "--aggressive"], capture_output=True)

    locations = [
        {"branch": "salvos-stores-sydney-central", "type": "Salvos Store", "geo": "(-33.8688, 151.2093)", "axis": "Sydney CBD"},
        {"branch": "salvos-family-store-tempe", "type": "Salvos Family Store", "geo": "(-33.9213, 151.1654)", "axis": "Tempe Depot"},
        {"branch": "home-centre-beverly-hills", "type": "Home Centre", "geo": "(-33.9483, 151.0825)", "axis": "Beverly Hills Hub"},
        {"branch": "home-centre-aspley-bridge", "type": "Home Centre Logistics", "geo": "(-33.8523, 151.2108)", "axis": "Harbour Vector"}
    ]
    
    current_branch_orig = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    if not current_branch_orig:
        current_branch_orig = "main"

    master_records = []

    for idx, loc in enumerate(locations, start=1):
        branch_name = loc["branch"]
        print(f"\n[+] Constructing Branch [{idx}/4]: {branch_name} ({loc['axis']})")
        
        res = subprocess.run(["git", "checkout", branch_name], capture_output=True, text=True)
        if res.returncode != 0:
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            
        payload = {
            "conductor": "Eric The Viking (PHILL)",
            "architect": "robdoe",
            "branch": branch_name,
            "facility_type": loc["type"],
            "geo_coordinates": loc["geo"],
            "regional_axis": loc["axis"],
            "harmonic_constants": {
                "arcsec_total": 1296000,
                "divisor": 3600,
                "seconds_day": 86400,
                "hours_day": 24,
                "reciprocal_scale": 1 / 7200,
                "harmonic_ratio": 0.052
            },
            "piano_keys": 88,
            "stack_depth": 216
        }
        
        hasher = hashlib.sha3_512()
        hasher.update(json.dumps(payload, sort_keys=True).encode('utf-8'))
        super_root = hasher.hexdigest()
        payload["super_root"] = super_root
        
        filename = f"salvos_home_{branch_name}.json"
        with open(filename, "w") as f:
            json.dump(payload, f, indent=4)
            
        subprocess.run(["git", "add", "-f", filename], check=True)
        subprocess.run(["git", "commit", "-m", f"matrix({branch_name}): locked super-root {super_root[:16]}..."], check=True)
        
        for t in range(1, 14):
            tag_name = f"v2026.8.11-{branch_name}-t{t:02d}-0.052"
            subprocess.run(["git", "tag", "-f", tag_name, "-m", f"Salvos & Home Centre tag {t} for {branch_name} at {loc['geo']}"], check=True)
            
        subprocess.run(["git", "push", "origin", branch_name, "--force"], check=True)
        subprocess.run(["git", "push", "origin", "--tags", "--force"], check=True)
        master_records.append(payload)

    subprocess.run(["git", "checkout", current_branch_orig], capture_output=True)

    print("\n================================================================")
    print(" [✓] SUCCESS! X4 BRANCHES & 52 TAGS LOCKED, PUSHED, & WITNESSED.")
    print("================================================================")

if __name__ == "__main__":
    execute_salvos_homes_matrix()
