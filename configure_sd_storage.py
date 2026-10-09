#!/usr/bin/env python3
import os
import json

def detect_and_configure_sd():
    print("================================================================")
    print("           TERMUX EXTERNAL SD CARD STORAGE BINDING              ")
    print("================================================================")
    
    # Common Termux external storage mount points or shared storage paths
    potential_paths = [
        "/storage/emulated/0",
        "/sdcard",
        "/storage/extSdCard",
        "/storage/sdcard1"
    ]
    
    # Check external storage directory in Termux (~/.termux/shared or standard /storage)
    termux_storage_dir = os.path.expanduser("~/storage")
    
    print("[*] Inspecting Termux storage shortcut links...")
    if os.path.exists(termux_storage_dir):
        print(f"[+] Found Termux storage root at: {termux_storage_dir}")
        items = os.listdir(termux_storage_dir)
        print(f"    -> Accessible folders: {items}")
    else:
        print("[!] Termux storage link not set up. Run 'termux-setup-storage' first if needed.")

    # Select target workspace storage
    target_sd_workspace = "/storage/emulated/0/robdoerootauthority"
    
    # Fallback to local home if external path isn't writable/mounted
    chosen_path = target_sd_workspace
    try:
        os.makedirs(chosen_path, exist_ok=True)
        test_file = os.path.join(chosen_path, ".write_test")
        with open(test_file, "w") as f:
            f.write("OK")
        os.remove(test_file)
        print(f"[+] Successfully verified write access to SD/Shared storage: {chosen_path}")
    except Exception as e:
        print(f"[!] Could not write to primary shared storage ({e}). Falling back to local home.")
        chosen_path = os.path.expanduser("~/robdoerootauthority")
        os.makedirs(chosen_path, exist_ok=True)

    config = {
        "active_storage_path": chosen_path,
        "node_id": "robertu",
        "status": "BOUND"
    }
    
    config_file = "storage_binding.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)
        
    print(f"[+] Storage binding profile saved to {config_file}")
    print(f"[+] Current active root -> {chosen_path}")
    print("================================================================")

if __name__ == "__main__":
    detect_and_configure_sd()
