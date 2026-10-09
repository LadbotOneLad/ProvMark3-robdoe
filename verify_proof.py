import hashlib
import json
import sys

def hash_leaf(data_string):
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

def compute_merkle_root(leaves):
    if not leaves:
        return None
    current_layer = [hash_leaf(leaf) for leaf in leaves]
    while len(current_layer) > 1:
        next_layer = []
        for i in range(0, len(current_layer), 2):
            left = current_layer[i]
            right = current_layer[i+1] if i + 1 < len(current_layer) else left
            combined = left + right
            parent_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
            next_layer.append(parent_hash)
        current_layer = next_layer
    return current_layer[0]

def verify_sovereign_proof(proof_filepath):
    print(f"[*] Loading proof file: {proof_filepath}")
    try:
        with open(proof_filepath, 'r') as f:
            proof_data = json.load(f)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {proof_filepath}")
        sys.exit(1)
        
    expected_root = proof_data.get("merkle_root")
    leaves = proof_data.get("leaves", [])
    hardware_anchor = proof_data.get("hardware_anchor", {})
    
    print(f"[*] Hardware Anchor Signature: {hardware_anchor.get('device_id', 'UNKNOWN')}")
    print(f"[*] Recalculating Merkle lattice from {len(leaves)} leaf nodes...")
    
    calculated_root = compute_merkle_root(leaves)
    
    print(f"    - Recorded Root:   {expected_root}")
    print(f"    - Calculated Root: {calculated_root}")
    
    if calculated_root == expected_root:
        print("\n[✔] STATUS: VERIFIED — BYZANTINE IMMUTABLE.")
        return True
    else:
        print("\n[✖] STATUS: FAILED — INTEGRITY MISMATCH.")
        return False

if __name__ == "__main__":
    success = verify_sovereign_proof("sovereign_lattice_proof.json")
    sys.exit(0 if success else 1)
