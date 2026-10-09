#!/usr/bin/env python3
import subprocess
import os

def git_transition():
    print("================================================================")
    print("          GIT REPOSITORY STAGE, COMMIT & PUSH PIPELINE          ")
    print("================================================================")
    
    # 1. Check if we are inside a git repository
    if not os.path.exists(".git"):
        print("[*] Initializing local Git repository...")
        subprocess.run(["git", "init"], check=True)
        
    # 2. Stage all updated orchestration and client scripts
    print("[*] Staging modified workspace files...")
    subprocess.run(["git", "add", "."], check=True)
    
    # 3. Commit changes with a descriptive timestamp message
    commit_msg = "feat: sync cellular mesh node orchestration and client pipelines"
    print(f"[*] Committing changes: '{commit_msg}'")
    
    # Check if there's anything to commit
    status_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status_res.stdout.strip():
        print("[+] Working tree clean. No new changes to commit.")
    else:
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        print("[+] Commit successful.")
        
    # 4. Push to remote repository if configured
    print("[*] Pushing updates to remote tracking branch...")
    push_res = subprocess.run(["git", "push"], capture_output=True, text=True)
    if push_res.returncode == 0:
        print("[+] Successfully pushed changes to remote repository!")
    else:
        print("[!] Git push skipped or requires upstream configuration.")
        print(f"    Details: {push_res.stderr.strip()}")
        
    print("================================================================")

if __name__ == "__main__":
    git_transition()
