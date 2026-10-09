#!/usr/bin/env python3
import subprocess

def setup_upstream_and_push():
    print("================================================================")
    print("          CONFIGURING UPSTREAM & PUSHING MESH STATE             ")
    print("================================================================")
    
    # Get current branch name
    branch_res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
    branch = branch_res.stdout.strip()
    print(f"[*] Current branch detected: {branch}")
    
    # Set upstream and push
    cmd = ["git", "push", "--set-upstream", "origin", branch]
    print(f"[*] Executing: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("[+] Successfully pushed branch with upstream tracking configured!")
        print(result.stdout)
    else:
        print("[!] Push encountered an issue:")
        print(result.stderr)
        print("\n[*] Tip: Ensure your remote repository ('origin') is configured and authenticated.")
        
    print("================================================================")

if __name__ == "__main__":
    setup_upstream_and_push()
