#!/usr/bin/env python3
import os
import json

def verify_shared_storage():
    print("================================================================")
    print("           VERIFYING TERMUX SHARED STORAGE                      ")
    print("================================================================")
    
    storage_root = os.path.expanduser("~/storage")
    shared_folder = os.path.join(storage_root, "shared")
    external_folder = os.path.join(storage_root, "external-1")
    
    target_path = None
    
    if os.path.exists(shared_folder):
        target_path = os.path.join(shared_folder, "robdoerootauthority")
    elif os.path.exists(external_folder):
        target_path = os.path.join(external_folder, "robdoerootauthority")
    else:
        # Fallback to direct emulated path if permission was granted manually
        target_path = "/storage/emulated/0/robdoerootauthority"
        
    print(f"[*] Testing target directory: {target_path}")
    
    try:
        os.makedirs(target_path, exist_ok=True)
        test_file = os.path.join(target_path, "sync_lock.test")
        with open(test_file, "w") as f:
            f.write("OK")
        os.remove(test_file)
        print(f"[+] SUCCESS: Write permission verified on shared/SD storage!")
        
        # Save binding configuration
        config = {
            "active_storage_path": target_path,
            "status": "BOUND_TO_SHARED"
        }
        with open("storage_binding.json", "w") as f:
            json.dump(config, f, indent=4)
            
        print(f"[+] Updated storage_binding.json -> {target_path}")
        
    except Exception as e:
        print(f"[!] Permission or path error: {e}")
        print("[!] Tip: If the permission dialog didn't pop up, run 'termux-setup-storage' manually in your terminal.")
        
    print("================================================================")

if __name__ == "__main__":
    verify_shared_storage()
