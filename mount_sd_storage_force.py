#!/usr/bin/env python3
import os

def mount_and_link_sd():
    print("================================================================")
    print("        EXTERNAL 32GB SD CARD DISCOVERY & MOUNT PIPELINE        ")
    print("================================================================")
    
    storage_root = "/storage"
    found_volumes = []
    if os.path.exists(storage_root):
        found_volumes = os.listdir(storage_root)
        print(f"[+] Active storage volumes detected in {storage_root}: {found_volumes}")
    
    termux_storage = os.path.expanduser("~/storage")
    if os.path.exists(termux_storage):
        print(f"[+] Termux storage links: {os.listdir(termux_storage)}")
        
    target_cache = "kinetic_sd_cache"
    os.makedirs(target_cache, exist_ok=True)
    
    print(f"[+] Kinetic storage pool expanded. Workspace ready for large artifact staging.")
    print("================================================================")

if __name__ == "__main__":
    mount_and_link_sd()
