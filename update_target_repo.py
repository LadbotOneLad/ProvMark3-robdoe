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
    login = subprocess.run(["gh", "api", "user", "-q", ".login"], capture_output=True, text=True).stdout.strip()
    print(f"[+] Authenticated GitHub user: {login}")
    
    run_cmd(["gh", "repo", "create", "AiAgency101", "--public", "--confirm"])
    run_cmd(["git", "remote", "set-url", "origin", f"https://github.com/{login}/AiAgency101.git"])
    run_cmd(["git", "branch", "-M", "master"])
    
    print("\n--- STAGE 1: Tagging Before Push ---")
    run_cmd(["git", "tag", "-f", "v2026.8.11-sxsyntax-pre-0.052", "-m", "Sxsyntax pre-push harmonic lock"])
    run_cmd(["git", "push", "origin", "tag", "v2026.8.11-sxsyntax-pre-0.052", "--force"])
    
    print("\n--- STAGE 2: Pushing Master Branch ---")
    run_cmd(["git", "push", "-u", "origin", "master", "--force"])
    
    print("\n--- STAGE 3: Tagging After Push ---")
    run_cmd(["git", "tag", "-f", "v2026.8.11-sxsyntax-post-0.052", "-m", "Sxsyntax post-push harmonic lock"])
    run_cmd(["git", "push", "origin", "tag", "v2026.8.11-sxsyntax-post-0.052", "--force"])
    
    print("\n[+] SUCCESS! Target repository correctly aligned under authenticated namespace.")

if __name__ == "__main__":
    main()
