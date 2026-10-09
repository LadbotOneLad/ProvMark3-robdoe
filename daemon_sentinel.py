#!/usr/bin/env python3
import time
import subprocess
import sys
import os
import logging

logging.basicConfig(
    filename="sentinel.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

TARGET_SCRIPT = "termux_daemon_manager.py"
MAX_RESTARTS = 5
RESTART_DELAY = 3

def supervise():
    restarts = 0
    while restarts < MAX_RESTARTS:
        logging.info(f"Launching target worker: {TARGET_SCRIPT} (Attempt {restarts + 1}/{MAX_RESTARTS})")
        print(f"[*] Sentinel spawning {TARGET_SCRIPT}...")
        
        process = subprocess.Popen([sys.executable, TARGET_SCRIPT])
        
        # Monitor the process health
        while process.poll() is None:
            time.sleep(2)
            
        exit_code = process.returncode
        logging.warning(f"Process exited with code {exit_code}")
        
        if exit_code == 0:
            print("[+] Process finished cleanly. Shutting down sentinel.")
            break
            
        restarts += 1
        print(f"[!] Process crashed. Restarting in {RESTART_DELAY}s...")
        time.sleep(RESTART_DELAY)
        
    if restarts >= MAX_RESTARTS:
        logging.error("Max restart threshold reached. Sentinel halting.")
        print("[!] Sentinel max restarts exceeded. Check sentinel.log.")

if __name__ == "__main__":
    supervise()
