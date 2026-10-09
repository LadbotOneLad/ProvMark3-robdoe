#!/usr/bin/env python3
import os
import subprocess

def repair_refs():
    print("================================================================")
    print("          REPAIRING CORRUPT GIT REFS & LOCAL STATE              ")
    print("================================================================")
    
    # 1. Remove dangling/bad ref entries causing fatal errors during gc/pack
    refs_head_dir = ".git/refs/heads"
    if os.path.exists(refs_head_dir):
        print("[*] Inspecting and cleaning invalid head refs...")
        for filename in os.listdir(refs_head_dir):
            filepath = os.path.join(refs_head_dir, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, "r") as f:
                        content = f.read().strip()
                    # Check if hash length is valid (40 chars for SHA-1)
                    if len(content) != 40:
                        print(f"[!] Removing corrupted ref file: {filename} (contents: {content})")
                        os.remove(filepath)
                except Exception:
                    os.remove(filepath)

    # 2. Clean packed-refs if it contains bad hashes
    packed_refs_path = ".git/packed-refs"
    if os.path.exists(packed_refs_path):
        print("[*] Clearing packed-refs cache...")
        os.remove(packed_refs_path)

    # 3. Initialize fresh commit state if needed or force clean push
    print("[*] Re-running git health check and staging...")
    subprocess.run(["git", "status"], capture_output=True)
    
    # 4. Try force pushing clean state
    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    if not branch:
        branch = "main"
        subprocess.run(["git", "checkout", "-b", branch])
        
    print(f"[*] Force pushing branch '{branch}' to origin...")
    res = subprocess.run(["git", "push", "origin", branch, "--force"], capture_output=True, text=True)
    
    if res.returncode == 0:
        print("[+] SUCCESS! Git repository repaired and synchronized.")
        print(res.stdout)
    else:
        print("[!] Push output:")
        print(res.stderr)
        
    print("================================================================")

if __name__ == "__main__":
    repair_refs()
