#!/usr/bin/env python3
import os
import shutil
import subprocess

def fix_cargo():
    print("================================================================")
    print("        CONFIGURING CARGO HOME TO EXTERNAL STORAGE              ")
    print("================================================================")
    
    sd_storage = "/storage/emulated/0/Android/data/com.termux/files/robdoerootauthority_storage"
    new_cargo_home = os.path.join(sd_storage, "cargo_home")
    os.makedirs(new_cargo_home, exist_ok=True)
    
    print(f"[*] Setting CARGO_HOME environment override to: {new_cargo_home}")
    
    # Clean up broken local symlink/dir
    local_cargo = os.path.expanduser("~/.cargo")
    if os.path.islink(local_cargo) or os.path.exists(local_cargo):
        shutil.rmtree(local_cargo, ignore_errors=True)
        
    os.symlink(new_cargo_home, local_cargo)
    print("[+] Linked ~/.cargo -> external storage cargo_home")
    
    # Configure cargo config or export variables
    shell_rc = os.path.expanduser("~/.bashrc")
    export_line = f'export CARGO_HOME="{new_cargo_home}"\n'
    
    with open(shell_rc, "a") as f:
        f.write(export_line)
        
    print("[+] CARGO_HOME export appended to .bashrc")
    print("================================================================")

if __name__ == "__main__":
    fix_cargo()
