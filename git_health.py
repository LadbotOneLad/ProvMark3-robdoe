import os
import subprocess

def run_git_health_check():
    print("[*] Running local repository health check...")
    
    if not os.path.exists(".git"):
        print("[!] Not a git repository. Initializing one...")
        subprocess.run(["git", "init"])
        subprocess.run(["git", "branch", "-M", "main"])
    
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    changes = result.stdout.strip().split("\n") if result.stdout.strip() else []
    
    print(f"[+] Detected {len(changes)} modified/untracked items.")
    
    for change in changes:
        if change:
            status, filename = change[:2].strip(), change[3:].strip()
            print(f"    -> [{status}] {filename}")

if __name__ == "__main__":
    run_git_health_check()
