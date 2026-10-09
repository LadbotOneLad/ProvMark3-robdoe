#!/usr/bin/env python3
import subprocess
import os

def fix_and_add():
    print("================================================================")
    print("          STACK 15 GIT ADD & SUBMODULE RECOVERY                 ")
    print("================================================================")
    
    # The error 128 during 'git add .' usually happens due to embedded 
    # git repositories or nested submodules cloned without proper handling.
    
    registry_dir = "stack_15_registry"
    if os.path.exists(registry_dir):
        print("[*] Converting cloned stack repositories into loose folders...")
        for item in os.listdir(registry_dir):
            item_path = os.path.join(registry_dir, item)
            git_folder = os.path.join(item_path, ".git")
            if os.path.exists(git_folder):
                print(f"    [-] Removing nested .git inside {item} to prevent git add conflict")
                subprocess.run(["rm", "-rf", git_folder], check=True)
                
    print("[*] Re-running git add safely...")
    subprocess.run(["git", "add", "stack_15_registry/"], check=True)
    
    # Commit changes
    print("[*] Committing Stack 15 integration...")
    commit_msg = "feat(stack-15): integrated Aussie public sector blueprints and Essential Eight controls cleanly"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    
    # Push update
    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    print(f"[*] Pushing stack to origin/{branch}...")
    res = subprocess.run(["git", "push", "origin", branch, "--force"], capture_output=True, text=True)
    
    if res.returncode == 0:
        print("[+] SUCCESS! Stack 15 successfully added, committed, and synced.")
    else:
        print(f"[!] Push result: {res.stderr.strip()}")
        
    print("================================================================")

if __name__ == "__main__":
    fix_and_add()
