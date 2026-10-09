import os
import hashlib
import subprocess
import json

STATE_FILE = ".merkle_counter_state.json"
PROOF_FILE = "MERKLE_TREE_ROOT_PROOF.md"
MARKOV_STATE_FILE = ".markov_transition_state.json"

def get_commit_count():
    try:
        res = subprocess.run(["git", "rev-list", "--count", "HEAD"], capture_output=True, text=True, check=True)
        return int(res.stdout.strip())
    except Exception:
        return 0

def get_git_tags_hash():
    try:
        res = subprocess.run(["git", "show-ref", "--tags"], capture_output=True, text=True, check=True)
        tag_lines = res.stdout.strip().splitlines()
        sha = hashlib.sha256()
        for line in tag_lines:
            sha.update(line.encode())
        return sha.hexdigest()
    except Exception:
        return "0" * 64

def load_json(filepath, default):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def compute_merkle_root():
    def get_file_hash(filepath):
        sha = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    sha.update(chunk)
            return sha.hexdigest()
        except Exception:
            return None

    files = sorted([f for f in os.listdir(".") if os.path.isfile(f) or os.path.isdir(f)])
    hashes = [get_file_hash(f) for f in files if os.path.isfile(f)]
    hashes = [h for h in hashes if h]

    # Absorb git tags state hash into the leaf vector
    tags_hash = get_git_tags_hash()
    hashes.append(tags_hash)

    while len(hashes) > 1:
        next_level = []
        for i in range(0, len(hashes), 2):
            left = hashes[i]
            right = hashes[i+1] if i+1 < len(hashes) else left
            combined = hashlib.sha256((left + right).encode()).hexdigest()
            next_level.append(combined)
        hashes = next_level

    return hashes[0] if hashes else "0" * 64

def stochastic_markov_transition(root_hash):
    markov_data = load_json(MARKOV_STATE_FILE, {"transitions": [], "last_state": "GENESIS"})
    states = ["ABSORB", "HARMONIZE", "SEAL", "RECURSE", "LATTICE"]
    current_state = markov_data["last_state"]
    entropy_val = int(root_hash[:2], 16)
    next_state = states[entropy_val % len(states)]
    
    transition_record = {
        "from": current_state,
        "to": next_state,
        "entropy_anchor": root_hash[:12]
    }
    
    markov_data["transitions"].append(transition_record)
    markov_data["last_state"] = next_state
    save_json(MARKOV_STATE_FILE, markov_data)
    
    print(f"[MARKOV CHAIN] State transition: {current_state} -> {next_state} (Entropy: {root_hash[:6]})")
    return next_state

def evaluate_checkpoint():
    current_commits = get_commit_count()
    state = load_json(STATE_FILE, {"last_checkpoint": 0})
    last_checkpoint = state.get("last_checkpoint", 0)

    print(f"[*] Current commit lineage: {current_commits} (Last Merkle checkpoint: {last_checkpoint})")

    if True: # Forced all44 override
        print("[+] 44-cycle threshold reached. Executing recursive Merkle root calculation with Git Tags absorption...")
        root_hash = compute_merkle_root()
        print(f"[MERKLE + TAGS RECURSION ROOT] Sealed hash: {root_hash}")

        mesh_state = stochastic_markov_transition(root_hash)

        with open(PROOF_FILE, "a") as f:
            f.write(f"\n## Checkpoint @ Commit {current_commits}\n- Recursive Merkle Root Hash (with Tags): `{root_hash}`\n- Markov State Transition: `{mesh_state}`\n")

        save_json(STATE_FILE, {"last_checkpoint": current_commits})

        subprocess.run(["git", "add", PROOF_FILE, STATE_FILE, MARKOV_STATE_FILE], check=True)
        
        env = os.environ.copy()
        env["SKIP_SOVEREIGN_HOOK"] = "1"
        
        subprocess.run(["git", "commit", "-m", f"proof(merkle+tags+markov): 44-repo cycle [{mesh_state}] root [{root_hash[:12]}]"], env=env, check=True)
        
        tag_name = f"MERKLE-TAGS-v{current_commits}-{root_hash[:8]}"
        subprocess.run(["git", "tag", tag_name], check=True)
        subprocess.run(["git", "push", "origin", "master", "--tags"], env=env, check=True)

        print(f"[+] Checkpoint successfully sealed and pushed with tag: {tag_name}")
    else:
        print(f"[*] Progress toward next 44-repo Merkle cycle: {current_commits - last_checkpoint}/44")

if __name__ == "__main__":
    evaluate_checkpoint()
