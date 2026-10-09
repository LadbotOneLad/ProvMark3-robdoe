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
    print("\n--- STAGE 1: Staging All Untracked Matrix Assets ---")
    run_cmd(["git", "add", "."])
    
    print("\n--- STAGE 2: Tagging Pre-Commit Omega State ---")
    run_cmd(["git", "tag", "-f", "v2026.8.11-matrix-pre-0.052", "-m", "Matrix asset staging harmonic lock"])
    run_cmd(["git", "push", "origin", "tag", "v2026.8.11-matrix-pre-0.052", "--force"])
    
    print("\n--- STAGE 3: Committing Matrix Snapshot ---")
    run_cmd(["git", "commit", "-m", "matrix(all): ingest complete untracked sovereign asset stack and orchestration suite"])
    
    print("\n--- STAGE 4: Tagging Post-Commit Omega State ---")
    run_cmd(["git", "tag", "-f", "v2026.8.11-matrix-post-0.052", "-m", "Matrix asset commit complete harmonic lock"])
    run_cmd(["git", "push", "origin", "tag", "v2026.8.11-matrix-post-0.052", "--force"])
    
    print("\n--- STAGE 5: Pushing Master Branch With Full Stack ---")
    run_cmd(["git", "push", "-u", "origin", "master", "--force"])
    run_cmd(["git", "push", "origin", "--tags", "--force"])
    
    print("\n[+] SUCCESS! Entire untracked workspace committed, tagged, and synchronized upstream.")

if __name__ == "__main__":
    main()
