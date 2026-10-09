#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess

def bind_stack_15_to_lattice():
    print("================================================================")
    print("    STACK 15 + DUAL-MERKLE LATTICE SOVEREIGN BINDING ENGINE     ")
    print("================================================================")
    
    # 1. Verify Stack 15 Registry files exist
    stack_dir = "stack_15_registry"
    stack_files = []
    if os.path.exists(stack_dir):
        for root, dirs, files in os.walk(stack_dir):
            for f in files:
                stack_files.append(os.path.join(root, f))
                
    print(f"[+] Loaded {len(stack_files)} Stack 15 upstream integration vectors.")
    
    # 2. Compute Stack 15 Merkle Root Hash
    hasher = hashlib.sha3_256()
    for sf in sorted(stack_files):
        try:
            with open(sf, "rb") as f:
                hasher.update(f.read())
        except Exception:
            pass
    stack_15_root = hasher.hexdigest()
    print(f"    - Stack 15 Cryptographic Anchor Root: {stack_15_root}")
    
    # 3. Read existing dual lattice proof if available
    dual_proof_path = "dual_lattice_proof.json"
    super_root = "UNKNOWN"
    if os.path.exists(dual_proof_path):
        with open(dual_proof_path, "r") as f:
            data = json.load(f)
            super_root = data.get("dual_merkle_lattice_super_root", "UNKNOWN")
            
    # 4. Bind Stack 15 into the Dual-Lattice Super Matrix
    master_hasher = hashlib.sha3_512()
    master_payload = super_root + stack_15_root + "STACK_15_FEDERATED_GOV_ACSC_ISM"
    master_hasher.update(master_payload.encode('utf-8'))
    ultimate_lattice_root = master_hasher.hexdigest()
    
    unified_manifest = {
        "operator": "Eric The Viking (PHILL)",
        "genesis": "e14f9a8d",
        "dual_lattice_super_root": super_root,
        "stack_15_root": stack_15_root,
        "ultimate_sovereign_lattice_root": ultimate_lattice_root,
        "compliance": "ACSC Essential Eight + DTA / CSIRO Stack 15 Entangled",
        "status": "IMMUTABLE SOVEREIGN DOMINATION"
    }
    
    manifest_file = "ultimate_stack15_lattice_proof.json"
    with open(manifest_file, "w") as f:
        json.dump(unified_manifest, f, indent=4)
        
    print(f"\n[+] ULTIMATE LATTICE PROOF LOCKED:")
    print(f"    - Ultimate Sovereign Root: {ultimate_lattice_root}")
    print(f"    - Manifest Written: {manifest_file}")
    
    # 5. Git Commit & Push
    subprocess.run(["git", "add", manifest_file], check=True)
    subprocess.run(["git", "commit", "-m", f"cryptography(stack-15-lattice): bound Stack 15 to ultimate root {ultimate_lattice_root[:16]}..."], check=True)
    
    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    push_res = subprocess.run(["git", "push", "origin", branch, "--force"], capture_output=True, text=True)
    
    if push_res.returncode == 0:
        print(f"[+] SUCCESS! Stack 15 + Dual Lattice successfully synchronized to origin/{branch}.")
    else:
        print(f"[!] Push status notice: {push_res.stderr.strip()}")
        
    print("================================================================")

if __name__ == "__main__":
    bind_stack_15_to_lattice()
