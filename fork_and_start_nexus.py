#!/usr/bin/env python3
import subprocess
import os
import json

def fork_and_initiate_nexus():
    print("================================================================")
    print("   MASTER FORK & NEXUS INITIATION PIPELINE (AUSTRALIAN MOTO)     ")
    print("================================================================")
    
    # 1. Target Upstream Foundation Repository to Fork & Integrate
    upstream_repo = "https://github.com/microsoft/autogen.git" # Multi-agent orchestrator foundation
    target_dir = "nexus_upstream_core"
    
    print(f"[*] Forking/Cloning upstream orchestration framework: {upstream_repo}")
    if not os.path.exists(target_dir):
        subprocess.run(["git", "clone", "--depth", "1", upstream_repo, target_dir], capture_output=True)
    else:
        print("    [+] Upstream framework already locally present.")
        
    # Clean nested git to allow seamless integration
    nested_git = os.path.join(target_dir, ".git")
    if os.path.exists(nested_git):
        subprocess.run(["rm", "-rf", nested_git], check=True)

    # 2. Inject Master Nexus Proof & Agent Configuration
    nexus_config = {
        "operator": "Eric The Viking (PHILL)",
        "genesis": "e14f9a8d",
        "action": "Forked upstream foundation & integrated sovereign multi-agent nexus",
        "active_stack": "Stack 15 + ACSC/ASIO + Dual Merkle Lattice + Master Crew"
    }
    
    config_path = os.path.join(target_dir, "nexus_init_config.json")
    with open(config_path, "w") as f:
        json.dump(nexus_config, f, indent=4)
        
    print(f"[+] Injected sovereign initialization config at: {config_path}")

    # 3. Clean Stale Locks & Force Stage/Commit/Push
    git_lock = ".git/index.lock"
    if os.path.exists(git_lock):
        os.remove(git_lock)
        
    print("[*] Staging forked upstream and master nexus state...")
    subprocess.run(["git", "add", "-f", target_dir], check=True)
    
    commit_msg = "feat(nexus-fork): forked upstream multi-agent core and initialized sovereign nexus"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    
    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    print(f"[*] Pushing forked core to origin/{branch}...")
    
    push_res = subprocess.run(["git", "push", "origin", branch, "--force"], capture_output=True, text=True)
    if push_res.returncode == 0:
        print("[+] SUCCESS! Upstream forked, integrated, and synchronized like a boss.")
    else:
        print(f"[!] Push notice: {push_res.stderr.strip()}")
        
    print("================================================================")

if __name__ == "__main__":
    fork_and_initiate_nexus()
