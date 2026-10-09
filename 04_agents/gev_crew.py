import json
import hashlib
import time

ACCOUNTS = ["LadbotoneLad", "backupsonbackups-cyber"]
MASTER_ROOT_SHA256 = "68421d52d990c5f0a395e592db43abae81d7ef2c052722cd9e56c1cddea240da"

def fold_recursive_merkle(acc1, acc2, root_hash):
    account_leaf = hashlib.sha256(f"{acc1}:{acc2}".encode()).hexdigest()
    unified_state = hashlib.sha256(f"{account_leaf}:{root_hash}".encode()).hexdigest()
    return account_leaf, unified_state

if __name__ == "__main__":
    acc_leaf, unified_root = fold_recursive_merkle(ACCOUNTS[0], ACCOUNTS[1], MASTER_ROOT_SHA256)
    
    proof = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "accounts": ACCOUNTS,
        "equality_status": "EQUAL_SOVEREIGN_TARGETS",
        "master_root_sha256": MASTER_ROOT_SHA256,
        "account_merkle_leaf": acc_leaf,
        "unified_recursive_root": unified_root
    }
    
    with open("MASTER_PROOF.json", "w") as f:
        json.dump(proof, f, indent=2)
        
    print(f"[+] Multi-Account Merkle Leaf: {acc_leaf}")
    print(f"[+] Unified Recursive Root:    {unified_root}")
    print(f"[+] State Absorbed & Written to MASTER_PROOF.json")
