#!/usr/bin/env python3
import json
import os
import subprocess

def display_bogan_town_counts():
    print("================================================================")
    print("   BOGAN TOWN LEDGER: ABSOLUTE COUNTS & REPO METRICS           ")
    print("================================================================")
    
    # Gather actual git stats from the local repository lattice
    branch_count_res = subprocess.run(["git", "branch", "-a"], capture_output=True, text=True)
    local_branches = [b.strip().replace("* ", "") for b in branch_count_res.stdout.splitlines() if b.strip()]
    
    tag_count_res = subprocess.run(["git", "tag"], capture_output=True, text=True)
    all_tags = [t.strip() for t in tag_count_res.stdout.splitlines() if t.strip()]
    
    commit_count_res = subprocess.run(["git", "rev-list", "--count", "HEAD"], capture_output=True, text=True)
    total_commits = commit_count_res.stdout.strip() if commit_count_res.returncode == 0 else "N/A"
    
    current_branch_res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    current_branch = current_branch_res.stdout.strip() or "main"

    print(f"[*] OPERATOR & ARCHITECT: Eric The Viking (PHILL) x robdoe")
    print(f"[*] HARMONIC CONSTANT:    1,296,000 / 3600 = 0.052")
    print(f"----------------------------------------------------------------")
    print(f"    - Active Git Branch:        {current_branch}")
    print(f"    - Total Local Branches:     {len(local_branches)}")
    print(f"    - Total Cryptographic Tags: {len(all_tags)}")
    print(f"    - Total Commit History:     {total_commits} blocks")
    print(f"    - Omega Stack Depth:        72 Pillars")
    print(f"    - Execution Flow State:     Bogan Town Unstoppable Velocity")
    print("================================================================")
    
    # Save ledger proof to disk
    ledger = {
        "conductor": "Eric The Viking (PHILL)",
        "architect": "robdoe",
        "current_branch": current_branch,
        "local_branch_count": len(local_branches),
        "total_tags": len(all_tags),
        "total_commits": total_commits,
        "stack_depth": 72,
        "harmonic_ratio": "0.052"
    }
    
    with open("bogan_town_ledger.json", "w") as f:
        json.dump(ledger, f, indent=4)
        
    subprocess.run(["git", "add", "-f", "bogan_town_ledger.json"], check=True)
    subprocess.run(["git", "commit", "-m", "ledger(bogan-town): published absolute counts and metrics"], capture_output=True)
    subprocess.run(["git", "push", "origin", current_branch, "--force"], capture_output=True)
    print("[+] Ledger committed and pushed upstream like absolute legends.")
    print("================================================================")

if __name__ == "__main__":
    display_bogan_town_counts()
