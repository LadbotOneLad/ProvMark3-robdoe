#!/usr/bin/env zsh
set -e

export SD_ROOT="/storage/B331-0B0C"
export TMPDIR="$SD_ROOT/pip_tmp"
export PIP_CACHE_DIR="$SD_ROOT/pip_cache"
export TMP="$SD_ROOT/git_tmp"
export TEMP="$SD_ROOT/git_tmp"
export GIT_OPTIONAL_LOCKS=0

mkdir -p "$TMPDIR" "$PIP_CACHE_DIR" "$TMP"

TAG_NAME="v1.0.0-dual-root"
COMMIT_HASH=$(git rev-parse HEAD 2>/dev/null || echo "0000000000000000000000000000000000000000")
TAG_HASH=$(git rev-parse "$TAG_NAME"^{tag} 2>/dev/null || git rev-parse "$TAG_NAME" 2>/dev/null || echo "0000000000000000000000000000000000000000")
TREE_HASH=$(git rev-parse HEAD^{tree} 2>/dev/null || echo "0000000000000000000000000000000000000000")

FS_HEX=$(find . -maxdepth 2 -not -path '*/.*' -type f -exec sha256sum {} + | sort | sha256sum | awk '{print $1}')

python3 - << PYEOF
import json, math, hashlib, os, time

commit_h = "$COMMIT_HASH"
tag_h    = "$TAG_HASH"
tree_h   = "$TREE_HASH"
fs_h     = "$FS_HEX"

raw_1024 = hashlib.sha512((commit_h + tag_h + tree_h + fs_h).encode()).hexdigest()
master_root = hashlib.sha256(raw_1024.encode()).hexdigest()

byte_arr = bytes.fromhex(master_root)
x = sum(byte_arr[0:10]) / (10 * 255)
y = sum(byte_arr[10:20]) / (10 * 255)
z = sum(byte_arr[20:30]) / (10 * 255)

prob = [master_root.count(c) / len(master_root) for c in set(master_root)]
entropy_3d = -sum(p * math.log2(p) for p in prob)

t_hours = (time.time() % 86400) / 3600.0
temporal_factor = math.exp(0.02 * t_hours)

w_divergence = math.pow(2, 1.5)

R_5D = math.sqrt(x**2 + y**2 + z**2 + (0.1 * t_hours)**2 + (0.5 * w_divergence)**2)

k1, k2 = 0.4, 0.1
phi_5d = R_5D / (1.0 + k1 * (R_5D**2) + k2 * (R_5D**4))

base_gas = 21000
gas_5d = math.ceil(
    base_gas * (1.0 + entropy_3d) * temporal_factor * (1.0 + 0.2 * w_divergence) * (1.0 / (phi_5d + 1e-6))
)

proof = {
    "node": "GENESIS:e14f9a8d",
    "accounts": ["LadbotoneLad", "backupsonbackups-cyber"],
    "tag_name": "$TAG_NAME",
    "tag_hash": tag_h,
    "commit_hash": commit_h,
    "tree_hash": tree_h,
    "fs_sha256": fs_h,
    "master_1024_root": master_root,
    "dimensions_5d": {
        "3d_spatial_entropy": round(entropy_3d, 4),
        "4d_temporal_hours": round(t_hours, 2),
        "5d_account_w": round(w_divergence, 2),
        "hyper_radius_R5D": round(R_5D, 4)
    },
    "fisheye_phi_5d": round(phi_5d, 4),
    "pure_termux_gas_5d": gas_5d
}

with open("PURE_TERMUX_5D_PROOF.json", "w") as f:
    json.dump(proof, f, indent=2)

print(json.dumps(proof, indent=2))
PYEOF
