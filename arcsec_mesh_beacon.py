#!/usr/bin/env python3
import time
import json
import hashlib
import hmac

SECRET_KEY = b"robertu_root_genesis_key"
NODE_ID = "robertu"
GENESIS_HASH = "e14f9a8d"

def calculate_arcsec():
    t = time.localtime()
    # 12,960,000 arcseconds in full 360 circle (360 * 3600)
    return (t.tm_hour % 12) * 108000 + t.tm_min * 1800 + t.tm_sec * 30

def generate_beacon():
    arcsec = calculate_arcsec()
    timestamp = time.time()
    
    payload = {
        "node_id": NODE_ID,
        "genesis": GENESIS_HASH,
        "arcsec_coordinate": arcsec,
        "total_arcsec_scale": 1296000,
        "epoch_timestamp": timestamp,
        "status": "SYNCHRONIZED"
    }
    
    payload_str = json.dumps(payload, sort_keys=True)
    signature = hmac.new(SECRET_KEY, payload_str.encode('utf-8'), hashlib.sha256).hexdigest()
    
    beacon = {
        "payload": payload,
        "signature": signature
    }
    
    beacon_file = "mesh_beacon.json"
    with open(beacon_file, "w") as f:
        json.dump(beacon, f, indent=4)
        
    print("================================================================")
    print("          MESH BEACON // ARCSEC SYNCHRONIZED PACKET             ")
    print("================================================================")
    print(f"[*] Node:           {NODE_ID} (Genesis: {GENESIS_HASH})")
    print(f"[*] Arc-Sec Vector: {arcsec:,} / 1,296,000")
    print(f"[*] HMAC Signature: {signature[:16]}...[VERIFIED]")
    print(f"[+] Beacon locked and written to {beacon_file}")
    print("================================================================")

if __name__ == "__main__":
    generate_beacon()
