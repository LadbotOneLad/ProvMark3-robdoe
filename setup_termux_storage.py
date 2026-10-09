#!/usr/bin/env python3
import subprocess
import os

def request_storage():
    print("================================================================")
    print("          INITIALIZING TERMUX STORAGE PERMISSIONS               ")
    print("================================================================")
    print("[*] Triggering Termux storage setup prompt...")
    print("[!] Please tap 'Allow' on your phone screen when the permission dialog appears.\n")
    
    # Run the official Termux storage configuration command
    subprocess.run(["termux-setup-storage"])
    
    storage_link = os.path.expanduser("~/storage")
    print(f"\n[*] Checking storage link path: {storage_link}")
    if os.path.lexists(storage_link):
        print("[+] Termux storage symlinks established successfully!")
        print("    -> You can now access shared storage via ~/storage/shared or ~/storage/external-1")
    else:
        print("[!] Storage symlink not detected yet. Ensure you granted permissions.")
    print("================================================================")

if __name__ == "__main__":
    request_storage()
