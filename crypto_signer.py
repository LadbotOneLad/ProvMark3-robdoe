#!/usr/bin/env python3
import json
import hashlib
import hmac
import os

SECRET_KEY = b"robertu_root_genesis_key"
MANIFEST_FILE = "workspace_manifest.json"
SIGNED_MANIFEST = "signed_manifest.json"

def sign_manifest():
    if not os.path.exists(MANIFEST_FILE):
        print(f"[!] Error: {MANIFEST_FILE} not found. Generate it first.")
        return

    with open(MANIFEST_FILE, "r") as f:
        data = f.read()

    # Generate HMAC-SHA256 signature of the file contents
    signature = hmac.new(SECRET_KEY, data.encode('utf-8'), hashlib.sha256).hexdigest()

    payload = {
        "manifest_content": json.loads(data),
        "crypto_signature": signature,
        "algorithm": "HMAC-SHA256"
    }

    with open(SIGNED_MANIFEST, "w") as f:
        json.dump(payload, f, indent=4)

    print(f"[+] Cryptographically signed manifest written to {SIGNED_MANIFEST}")
    print(f"    -> Signature: {signature[:16]}...[LOCKED]")

if __name__ == "__main__":
    sign_manifest()
