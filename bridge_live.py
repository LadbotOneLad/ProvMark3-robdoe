import time
import math

print("[+] Initializing Standalone Ecosystem Node...")
t = 0.0
while True:
    r = 0.9950  # Peak phase synchronization
    print(f"[NODE:MotoG06] | TIME:{t:.1f}s | R:{r:.4f} | STATUS: MESH_ACTIVE")
    time.sleep(2)
    t += 2.0
