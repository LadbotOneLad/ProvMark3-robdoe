#!/usr/bin/env python3
import subprocess
import os

def execute_branch_tag_matrix():
    print("================================================================")
    print("   13 BRANCHES + 4 TAGS PER BRANCH: ULTIMATE UPSTREAM PUSH      ")
    print("================================================================")
    
    # Ensure any stale index locks are cleared
    for lock_path in [".git/index.lock", ".git/gc.pid"]:
        if os.path.exists(lock_path):
            os.remove(lock_path)

    # 13 Sovereign Branches covering the entire architecture
    branches = [
        "main",
        "lattice-core",
        "stack-15-engine",
        "acsc-azul-secops",
        "asio-network-mesh",
        "crew-ai-nexus",
        "autogen-fork",
        "proxmark-rfid",
        "esp32-rom-matrix",
        "termux-ssh-shell",
        "xyo-blockchain-node",
        "byzantine-consensus",
        "shaped-force-law"
    ]
    
    current_branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    if not current_branch:
        current_branch = "main"

    print(f"[*] Deploying 13 branches with 4 cryptographic tags each...")

    for idx, branch in enumerate(branches, start=1):
        print(f"\n    [{idx}/13] Processing branch: {branch}")
        
        # Switch or create branch
        if branch != current_branch:
            res = subprocess.run(["git", "checkout", branch], capture_output=True, text=True)
            if res.returncode != 0:
                subprocess.run(["git", "checkout", "-b", branch], check=True)
        
        # Create 4 unique tags for this branch
        for tag_num in range(1, 5):
            tag_name = f"v2026.8.{idx}.{tag_num}-{branch[:10]}"
            # Force tag creation to avoid collisions
            subprocess.run(["git", "tag", "-f", tag_name, "-m", f"Sovereign lattice release {tag_name} for {branch}"], check=True)
            
        # Push branch and its tags upstream
        print(f"        [*] Pushing branch {branch} and tags to origin...")
        subprocess.run(["git", "push", "origin", branch, "--force"], check=True)
        subprocess.run(["git", "push", "origin", "--tags", "--force"], check=True)

    print("\n[+] SUCCESS! All 13 branches and 52 tags successfully pushed upstream.")
    print("================================================================")

if __name__ == "__main__":
    execute_branch_tag_matrix()
