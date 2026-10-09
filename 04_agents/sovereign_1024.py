import hashlib
import json
import time

def sha512_hex(data: str) -> str:
    return hashlib.sha512(data.encode('utf-8')).hexdigest()

def sha1024_fold(data: str) -> str:
    h1 = sha512_hex(f"LEFT:{data}")
    h2 = sha512_hex(f"RIGHT:{data}")
    return f"{h1}{h2}"

def compute_sovereign_1024_state(acc1: str, acc2: str, master_root: str):
    leaf1 = sha1024_fold(f"SOVEREIGN_ACC_1:{acc1}")
    leaf2 = sha1024_fold(f"SOVEREIGN_ACC_2:{acc2}")
    
    account_node = sha1024_fold(f"{leaf1}:{leaf2}")
    unified_1024_root = sha1024_fold(f"{account_node}:{master_root}")
    
    print(f"[+] Leaf 1 (1024-bit) : {leaf1[:32]}...{leaf1[-32:]}")
    print(f"[+] Leaf 2 (1024-bit) : {leaf2[:32]}...{leaf2[-32:]}")
    print(f"[+] Root   (1024-bit) : {unified_1024_root}")
    
    return unified_1024_root

if __name__ == "__main__":
    ACCOUNTS = ["LadbotoneLad", "backupsonbackups-cyber"]
    MASTER_ROOT = "68421d52d990c5f0a395e592db43abae81d7ef2c052722cd9e56c1cddea240da"
    
    root_1024 = compute_sovereign_1024_state(ACCOUNTS[0], ACCOUNTS[1], MASTER_ROOT)
    
    proof_1024 = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "accounts": ACCOUNTS,
        "equality_status": "EQUAL_SOVEREIGN_TARGETS",
        "master_root_sha256": MASTER_ROOT,
        "unified_1024_root": root_1024
    }
    
    with open("MASTER_PROOF_1024.json", "w") as f:
        json.dump(proof_1024, f, indent=2)
