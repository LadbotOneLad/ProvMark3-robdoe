import os
import hashlib
import datetime

ROOT = os.path.expanduser("~/robdoerootauthority")
LEDGER = os.path.join(ROOT, "robdoe_witness.log")

os.makedirs(ROOT, exist_ok=True)

def ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def hash_block(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def witness(source: str, kind: str, payload: str):
    raw = f"{ts()} | {source} | {kind} | {payload}"
    block_hash = hash_block(raw)
    line = f"{raw} | HASH:{block_hash}\n"

    with open(LEDGER, "a") as f:
        f.write(line)

    return block_hash
