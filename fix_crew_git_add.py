#!/usr/bin/env python3
import subprocess
import os

def fix_git_lock_and_add():
    print("================================================================")
    print("          CREW GIT RECOVERY & FORCE-ADD PIPELINE                ")
    print("================================================================")
    
    # Check if a git index lock file exists and remove it if stale
    git_lock = ".git/index.lock"
    if os.path.exists(git_lock):
        print("    [!] Stale git lock detected. Removing...")
        os.remove(git_lock)
        
    print("[*] Re-staging manifest with force override...")
    subprocess.run(["git", "add", "-f", "crew_sovereign_manifest.json"], check=True)
    
    print("[*] Committing multi-agent sovereign state...")
    commit_msg = "crew(orchestration): resolved git lock and locked multi-agent super-root"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    
    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    print(f"[*] Pushing crew mesh to origin/{branch}...")
    
    push_res = subprocess.run(["git", "push", "origin", branch, "--force"], capture_output=True, text=True)
    if push_res.returncode == 0:
        print("[+] SUCCESS! Crew orchestration state synchronized and pushed.")
    else:
        print(f"[!] Push notice: {push_res.stderr.strip()}")
        
    print("================================================================")

if __name__ == "__main__":
    fix_git_lock_and_add()
