#!/usr/bin/env python3
import os
import shutil
import subprocess

def clean_storage():
    print("================================================================")
    print("        EMERGENCY DISK SPACE & CARGO CACHE CLEANUP              ")
    print("================================================================")
    
    # 1. Check disk space before
    print("[*] Disk usage before cleanup:")
    subprocess.run(["df", "-h", "/data/data/com.termux/files/home"])
    
    # 2. Clear cargo cache & registry to fix 'No space left on device'
    cargo_home = os.path.expanduser("~/.cargo")
    if os.path.exists(cargo_home):
        print(f"[*] Purging Cargo registry and cache in {cargo_home}...")
        registry_cache = os.path.join(cargo_home, "registry")
        if os.path.exists(registry_cache):
            shutil.rmtree(registry_cache, ignore_errors=True)
            print("[+] Cargo registry cache cleared.")
            
    # 3. Clear pip cache
    print("[*] Clearing pip cache...")
    subprocess.run(["pip", "cache", "purge"], stderr=subprocess.DEVNULL)
    
    # 4. Clear temporary files
    tmp_dir = "/data/data/com.termux/files/usr/tmp"
    if os.path.exists(tmp_dir):
        print("[*] Clearing Termux temp files...")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        os.makedirs(tmp_dir, exist_ok=True)
        
    # 5. Check disk space after
    print("\n[*] Disk usage after cleanup:")
    subprocess.run(["df", "-h", "/data/data/com.termux/files/home"])
    print("================================================================")

if __name__ == "__main__":
    clean_storage()
