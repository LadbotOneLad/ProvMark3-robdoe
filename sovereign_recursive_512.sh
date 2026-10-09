#!/usr/bin/env bash
set -euo pipefail

ACCOUNT_1="LadbotoneLad"
ACCOUNT_2="backupsonbackups-cyber"
MANUAL_REPOS_ACC2=()

OUTPUT_FILE="RECURSIVE_MASTER_PROOF.json"
SIG_FILE="RECURSIVE_MASTER_PROOF.json.sig"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[+] Sovereign Recursive Multi-Layer Hash Engine"
echo "[+] Primitive: SHA-512 Recursive Merkle Tree"
echo "[+] Timestamp: $TIMESTAMP"

WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

# Function: Recursively hash a directory tree using SHA-512
compute_recursive_tree_hash() {
    local target_dir="$1"
    # Find all files, sort deterministically, compute SHA-512 per file, then hash the aggregate
    find "$target_dir" -type f ! -path '*/.git/*' -print0 | \
        LC_ALL=C sort -z | \
        xargs -0 sha512sum 2>/dev/null | \
        sha512sum | awk '{print $1}'
}

MANIFEST_TMP="$WORK_DIR/manifest.tmp"
touch "$MANIFEST_TMP"

process_repo() {
    local account="$1"
    local repo_url="$2"
    local repo_name
    repo_name=$(basename "$repo_url" .git)

    echo "    ├─ Recursive SHA-512 Hashing: $repo_name"
    git clone --quiet "$repo_url" "$WORK_DIR/clones/$repo_name" 2>/dev/null || return 0

    local commit_hash tree_sha512
    commit_hash=$(git --git-dir="$WORK_DIR/clones/$repo_name/.git" rev-parse HEAD 2>/dev/null || echo "empty")

    if [ "$commit_hash" != "empty" ]; then
        tree_sha512=$(compute_recursive_tree_hash "$WORK_DIR/clones/$repo_name")
    else
        tree_sha512="empty_repository_node"
    fi

    cat <<JEOF >> "$MANIFEST_TMP"
  {
    "account": "$account",
    "repository": "$repo_name",
    "head_commit": "$commit_hash",
    "recursive_sha512_root": "$tree_sha512"
  },
JEOF
    rm -rf "$WORK_DIR/clones/$repo_name"
}

mkdir -p "$WORK_DIR/clones"

# 1. Sweep Account 1
echo -e "\n[>] Processing Account Node: $ACCOUNT_1"
repos1=$(curl -s "https://api.github.com/users/$ACCOUNT_1/repos?per_page=100" | grep -o '"clone_url": "[^"]*' | cut -d'"' -f4 || true)
for repo_url in $repos1; do
    process_repo "$ACCOUNT_1" "$repo_url"
done

# 2. Sweep Account 2
echo -e "\n[>] Processing Account Node: $ACCOUNT_2"
if [ ${#MANUAL_REPOS_ACC2[@]} -gt 0 ]; then
    for repo_name in "${MANUAL_REPOS_ACC2[@]}"; do
        process_repo "$ACCOUNT_2" "https://github.com/$ACCOUNT_2/$repo_name.git"
    done
fi

# Construct Layer 2 JSON
echo "[" > "$WORK_DIR/final_manifest.json"
if [ -s "$MANIFEST_TMP" ]; then
    sed '$ s/,$//' "$MANIFEST_TMP" >> "$WORK_DIR/final_manifest.json"
fi
echo "]" >> "$WORK_DIR/final_manifest.json"

# Master SHA-512 Root calculation over the combined recursive manifest
RECURSIVE_MASTER_ROOT=$(sha512sum "$WORK_DIR/final_manifest.json" | awk '{print $1}')

cat <<JEOF > "$OUTPUT_FILE"
{
  "specification": "Sovereign-Recursive-Merkle-v1",
  "hash_algorithm": "SHA-512",
  "timestamp_utc": "$TIMESTAMP",
  "accounts": ["$ACCOUNT_1", "$ACCOUNT_2"],
  "recursive_master_sha512": "$RECURSIVE_MASTER_ROOT",
  "state_tree": $(cat "$WORK_DIR/final_manifest.json")
}
JEOF

echo -e "\n===================================================================================================="
echo " RECURSIVE MASTER SHA-512 ROOT:"
echo " $RECURSIVE_MASTER_ROOT"
echo "===================================================================================================="

KEY_PATH="$HOME/.ssh/id_ed25519"
if [ -f "$KEY_PATH" ]; then
    ssh-keygen -Y sign -f "$KEY_PATH" -n file "$OUTPUT_FILE" 2>/dev/null && \
    echo "[+] ED25519 Signature attached: $SIG_FILE"
fi
