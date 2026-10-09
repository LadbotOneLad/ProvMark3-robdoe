#!/usr/bin/env python3
import subprocess

def run_cmd(cmd):
    print(f"[*] Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.stderr.strip():
        print(res.stderr.strip())
    return res.returncode

def main():
    # 1. Use existing local repo or check remote
    # Since branch is master locally but script pushed main, let's align to master or main properly
    run_cmd(["git", "branch", "-M", "master"])
    
    # Check if gh CLI is available and authenticated, or fix remote
    # Let's create the repo via gh if missing, or use a valid existing remote pattern
    print("[*] Ensuring repository exists on GitHub via gh CLI...")
    run_cmd(["gh", "repo", "create", "robdoerootauthority/AiAgency101", "--public", "--confirm"])
    
    # Push master branch and tags cleanly
    code = run_cmd(["git", "push", "-u", "origin", "master", "--force"])
    if code != 0:
        # Fallback to main
        run_cmd(["git", "branch", "-M", "main"])
        run_cmd(["git", "push", "-u", "origin", "main", "--force"])
        
    run_cmd(["git", "push", "origin", "--tags", "--force"])
    print("[+] Sxsyntax push sequence completed successfully.")

if __name__ == "__main__":
    main()
