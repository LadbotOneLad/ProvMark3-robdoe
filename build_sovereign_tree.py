#!/data/data/com.termux/files/usr/bin/env python3
import os
import hashlib
import json
import subprocess

def compute_sha256(filepath):
    """Compute SHA-256 hash of a single file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def get_dir_merkle_node(dir_path):
    """Recursively build Merkle tree nodes for a directory structure."""
    children = []
    
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return None

    for entry in entries:
        if entry in ['.git', '__pycache__', 'node_modules', '.cache']:
            continue
            
        full_path = os.path.join(dir_path, entry)
        
        if os.path.islink(full_path):
            continue
        elif os.path.isfile(full_path):
            file_hash = compute_sha256(full_path)
            if file_hash:
                children.append({
                    "name": entry,
                    "type": "file",
                    "hash": file_hash
                })
        elif os.path.isdir(full_path):
            sub_node = get_dir_merkle_node(full_path)
            if sub_node and sub_node.get("children"):
                children.append({
                    "name": entry,
                    "type": "directory",
                    "hash": sub_node["hash"],
                    "children": sub_node["children"]
                })

    combined = "".join(c["hash"] for c in children).encode('utf-8')
    node_hash = hashlib.sha256(combined).hexdigest() if combined else hashlib.sha256(b"empty").hexdigest()

    return {
        "hash": node_hash,
        "children": children
    }

def main():
    root_dir = os.path.expanduser("~/robdoerootauthority")
    print(f"[*] Scanning workspace root: {root_dir}")

    merkle_tree = get_dir_merkle_node(root_dir)
    master_root_hash = merkle_tree["hash"]

    manifest = {
        "title": "Sovereign Root Authority Merkle Manifest",
        "master_root_sha256": master_root_hash,
        "tree": merkle_tree
    }

    manifest_path = os.path.join(root_dir, "MASTER_SOVEREIGN_MANIFEST.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"[+] Manifest generated: {manifest_path}")
    print(f"[=] MASTER MERKLE ROOT SHA-256: {master_root_hash}")

    key_path = os.path.expanduser("~/.ssh/id_ed25519")
    if os.path.exists(key_path):
        print("[*] Signing manifest with local ED25519 key...")
        cmd = ["ssh-keygen", "-Y", "sign", "-f", key_path, "-n", "file", manifest_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[+] Signed successfully: {manifest_path}.sig")
        else:
            print(f"[-] Signing error: {res.stderr}")

if __name__ == "__main__":
    main()
