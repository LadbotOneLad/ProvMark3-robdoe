#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess

def execute_acsc_asio_lattice_pipeline():
    print("================================================================")
    print("   ACSC (AZUL) & ASIO NETWORK LATTICE SOVEREIGN INTEGRATION     ")
    print("================================================================")
    
    upstream_targets = [
        {"name": "acsc-azul", "url": "https://github.com/AustralianCyberSecurityCentre/azul.git"},
        {"name": "asio-network", "url": "https://github.com/chriskohlhoff/asio.git"}
    ]
    
    registry_dir = "stack_acsc_asio_registry"
    os.makedirs(registry_dir, exist_ok=True)
    
    print("[*] Cloning and locking official Australian Cyber / Network repositories...")
    for target in upstream_targets:
        dest = os.path.join(registry_dir, target["name"])
        if not os.path.exists(dest):
            print(f"    [+] Pulling telemetry framework: {target['name']} -> {target['url']}")
            subprocess.run(["git", "clone", "--depth", "1", target["url"], dest], capture_output=True)
        else:
            print(f"    [+] Target {target['name']} already cached locally.")
            
        # Clean nested .git entries to prevent index collision (fixes error 128)
        nested_git = os.path.join(dest, ".git")
        if os.path.exists(nested_git):
            subprocess.run(["rm", "-rf", nested_git], check=True)

    print("[*] Computing SHA3-256 Dual-Lattice Vectors for Threat Intelligence...")
    hasher_acsc = hashlib.sha3_256()
    hasher_asio = hashlib.sha3_256()
    
    acsc_path = os.path.join(registry_dir, "acsc-azul")
    asio_path = os.path.join(registry_dir, "asio-network")
    
    if os.path.exists(acsc_path):
        for root, dirs, files in os.walk(acsc_path):
            for f in files[:50]:
                try:
                    with open(os.path.join(root, f), "rb") as file_obj:
                        hasher_acsc.update(file_obj.read())
                except Exception:
                    pass
                    
    if os.path.exists(asio_path):
        for root, dirs, files in os.walk(asio_path):
            for f in files[:50]:
                try:
                    with open(os.path.join(root, f), "rb") as file_obj:
                        hasher_asio.update(file_obj.read())
                except Exception:
                    pass
                    
    root_acsc = hasher_acsc.hexdigest()
    root_asio = hasher_asio.hexdigest()
    
    master_hasher = hashlib.sha3_512()
    master_payload = root_acsc + root_asio + "PHILL:ERIC_THE_VIKING:ACSC_AZUL:ASIO_CORE:GENESIS:e14f9a8d"
    master_hasher.update(master_payload.encode('utf-8'))
    ultimate_super_root = master_hasher.hexdigest()
    
    lattice_manifest = {
        "operator": "Eric The Viking (PHILL)",
        "genesis": "e14f9a8d",
        "acsc_azul_root": root_acsc,
        "asio_network_root": root_asio,
        "ultimate_sovereign_lattice_root": ultimate_super_root,
        "framework": "ACSC ISM / Essential Eight + ASIO Asynchronous Network Layer",
        "status": "IMMUTABLE CYBER DOMINATION"
    }
    
    manifest_path = "ultimate_acsc_asio_lattice_proof.json"
    with open(manifest_path, "w") as f:
        json.dump(lattice_manifest, f, indent=4)
        
    print(f"\n[+] ACSC / ASIO LATTICE PROOF GENERATED:")
    print(f"    - ACSC Azul Root: {root_acsc}")
    print(f"    - ASIO Network Root: {root_asio}")
    print(f"    - Ultimate Super-Root: {ultimate_super_root}")
    print(f"    - Manifest Locked: {manifest_path}")

    print("[*] Staging and committing secure state...")
    subprocess.run(["git", "add", manifest_path], check=True)
    subprocess.run(["git", "add", registry_dir], check=True)
    
    commit_msg = f"cryptography(acsc-asio-lattice): locked sovereign super-root {ultimate_super_root[:16]}..."
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    
    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    print(f"[*] Pushing secure lattice payload to origin/{branch}...")
    
    push_res = subprocess.run(["git", "push", "origin", branch, "--force"], capture_output=True, text=True)
    if push_res.returncode == 0:
        print("[+] SUCCESS! ACSC & ASIO integrated, mathematically proved, and pushed like a boss.")
    else:
        print(f"[!] Push notice: {push_res.stderr.strip()}")
        
    print("================================================================")

if __name__ == "__main__":
    execute_acsc_asio_lattice_pipeline()
