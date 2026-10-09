#!/usr/bin/env python3
import os
import subprocess

def clean_workspace():
    print("[*] Initiating repository hygiene scan...")
    
    # Extensions or files to clean up
    target_extensions = ['.log', '.bak', '.tmp', '.sarif']
    removed_count = 0

    for root, dirs, files in os.walk('.'):
        # Skip hidden git directory
        if '.git' in root:
            continue
        for file in files:
            if any(file.endswith(ext) for ext in target_extensions):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"[-] Removed temp artifact: {file_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"[!] Failed to remove {file_path}: {e}")

    print(f"[+] Cleanup complete. Removed {removed_count} temporary files.")

    # Run a quick git status check
    print("\n[*] Current Git Status:")
    result = subprocess.run(["git", "status", "-s"], capture_output=True, text=True)
    print(result.stdout if result.stdout else "Working tree clean.")

if __name__ == "__main__":
    clean_workspace()
