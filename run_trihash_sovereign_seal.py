import os
import hashlib
import subprocess
import json

SEAL_PROOF_FILE = "SOVEREIGN_TRINITY_SEAL.md"
PLEROMA_STATE = ".pleroma_fractal_state.json"
PROOF_FILE = "MERKLE_TREE_ROOT_PROOF.md"

def get_git_head_hash():
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "0" * 40

def compute_trihash_seal():
    # 1. Gather Git Head
    head_hash = get_git_head_hash()
    
    # 2. Gather Pleroma Fractal Hash
    pleroma_hash = "0" * 64
    if os.path.exists(PLEROMA_STATE):
        with open(PLEROMA_STATE, "r") as f:
            data = json.load(f)
            pleroma_hash = data.get("latest_fractal_hash", "0" * 64)
            
    # 3. Gather Merkle Root Proof Tail
    merkle_tail = "0" * 64
    if os.path.exists(PROOF_FILE):
        with open(PROOF_FILE, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.read()
            merkle_tail = hashlib.sha256(size).hexdigest()

    # Combine into Trihash Trinity Root
    trinity_payload = f"{head_hash}:{pleroma_hash}:{merkle_tail}".encode()
    trinity_seal = hashlib.sha256(trinity_payload).hexdigest()
    
    print(f"[TRINITY SEAL] Unified Sovereign Trihash: {trinity_seal}")
    return head_hash, pleroma_hash, trinity_seal

def execute_trinity_seal():
    head, pleroma, seal = compute_trihash_seal()
    
    seal_entry = f"\n## Trinity Seal @ HEAD `{head[:12]}`\n- Pleroma Manifold: `{pleroma[:16]}...`\n- Unified Trihash Seal: `{seal}`\n"
    
    with open(SEAL_PROOF_FILE, "a") as f:
        f.write(seal_entry)
        
    print(f"[+] Sovereign Trinity Seal written to {SEAL_PROOF_FILE}")

if __name__ == "__main__":
    execute_trinity_seal()
