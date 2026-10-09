#!/usr/bin/env python3
import os
import shutil
import subprocess

def purge_and_optimize():
    print("================================================================")
    print("      EMERGENCY INTERNAL STORAGE PURGE & GIT COMPACTION         ")
    print("================================================================")
    
    # 1. Prune heavy cloned registries to free up internal storage block limits
    heavy_dirs = [
        "mastery_forks_registry",
        "stack_acsc_asio_registry",
        "stack_15_registry",
        "nexus_upstream_core"
    ]
    
    for d in heavy_dirs:
        if os.path.exists(d):
            print(f"    [-] Purging heavy local clone directory: {d}")
            shutil.rmtree(d, ignore_errors=True)
            
    # 2. Clean git object pack bloat and stale locks
    print("[*] Running git garbage collection and pruning loose objects...")
    subprocess.run(["git", "gc", "--prune=all", "--aggressive"], capture_output=True)
    
    git_lock = ".git/index.lock"
    if os.path.exists(git_lock):
        os.remove(git_lock)
        
    total, used, free = shutil.disk_usage('/')
    print(f"[+] Storage status: {free // (2**20)} MB free available.")
    print("================================================================")

if __name__ == "__main__":
    purge_and_optimize()
