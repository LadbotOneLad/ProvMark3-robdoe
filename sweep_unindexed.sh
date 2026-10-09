#!/usr/bin/env bash
set -euo pipefail

ACCOUNT_1="LadbotoneLad"
ACCOUNT_2="backupsonbackups-cyber"

# Explicit list of repos under backupsonbackups-cyber
# Add any repo names here separated by space: e.g. ("repo1" "repo2" "my-project")
MANUAL_REPOS_ACC2=()

OUTPUT_FILE="MASTER_PROOF.json"
SIG_FILE="MASTER_PROOF.json.sig"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[+] Sovereign Multi-Account Cryptographic Sweep"
echo "[+] Target 1: $ACCOUNT_1 (API Discovery)"
echo "[+] Target 2: $ACCOUNT_2 (Direct & API Discovery)"
echo "[+] Timestamp: $TIMESTAMP"

WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

echo "[" > "$WORK_DIR/manifest.tmp"

# 1. Sweep LadbotoneLad via API
echo -e "\n[>] Sweeping account: $ACCOUNT_1..."
repos1=$(curl -s "https://api.github.com/users/$ACCOUNT_1/repos?per_page=100" | grep -o '"clone_url": "[^"]*' | cut -d'"' -f4 || true)

for repo_url in $repos1; do
    repo_name=$(basename "$repo_url" .git)
    echo "    ├─ Hashing: $repo_name"
    
    git clone --bare -q "$repo_url" "$WORK_DIR/$repo_name.git" 2>/dev/null || continue
    commit_hash=$(git --git-dir="$WORK_DIR/$repo_name.git" rev-parse HEAD 2>/dev/null || echo "empty")
    
    if [ "$commit_hash" != "empty" ]; then
        tree_sha=$(git --git-dir="$WORK_DIR/$repo_name.git" ls-tree -r HEAD 2>/dev/null | sha256sum | awk '{print $1}')
    else
        tree_sha="empty_repo"
    fi

    cat <<JEOF >> "$WORK_DIR/manifest.tmp"
  {
    "account": "$ACCOUNT_1",
    "repository": "$repo_name",
    "head_commit": "$commit_hash",
    "tree_sha256_root": "$tree_sha"
  },
JEOF
    rm -rf "$WORK_DIR/$repo_name.git"
done

# 2. Sweep backupsonbackups-cyber (Manual List + Direct Clones)
echo -e "\n[>] Sweeping account: $ACCOUNT_2..."
if [ ${#MANUAL_REPOS_ACC2[@]} -eq 0 ]; then
    echo "    └─ No manual repos specified in MANUAL_REPOS_ACC2 array."
else
    for repo_name in "${MANUAL_REPOS_ACC2[@]}"; do
        repo_url="https://github.com/$ACCOUNT_2/$repo_name.git"
        echo "    ├─ Hashing Direct Target: $repo_name"
        
        git clone --bare -q "$repo_url" "$WORK_DIR/$repo_name.git" 2>/dev/null || {
            echo "    │  └─ Could not clone $repo_url (empty or uncreated)"
            continue
        }
        
        commit_hash=$(git --git-dir="$WORK_DIR/$repo_name.git" rev-parse HEAD 2>/dev/null || echo "empty")
        
        if [ "$commit_hash" != "empty" ]; then
            tree_sha=$(git --git-dir="$WORK_DIR/$repo_name.git" ls-tree -r HEAD 2>/dev/null | sha256sum | awk '{print $1}')
        else
            tree_sha="empty_repo"
        fi

        cat <<JEOF >> "$WORK_DIR/manifest.tmp"
  {
    "account": "$ACCOUNT_2",
    "repository": "$repo_name",
    "head_commit": "$commit_hash",
    "tree_sha256_root": "$tree_sha"
  },
JEOF
        rm -rf "$WORK_DIR/$repo_name.git"
    done
fi

sed -i '$ s/,$//' "$WORK_DIR/manifest.tmp"
echo "]" >> "$WORK_DIR/manifest.tmp"

MASTER_ROOT_HASH=$(sha256sum "$WORK_DIR/manifest.tmp" | awk '{print $1}')

cat <<JEOF > "$OUTPUT_FILE"
{
  "specification": "Sovereign-State-v1",
  "timestamp_utc": "$TIMESTAMP",
  "accounts": ["$ACCOUNT_1", "$ACCOUNT_2"],
  "master_root_sha256": "$MASTER_ROOT_HASH",
  "state_tree": $(cat "$WORK_DIR/manifest.tmp")
}
JEOF

echo -e "\n=================================================="
echo " MASTER ROOT SHA-256: $MASTER_ROOT_HASH"
echo "=================================================="

KEY_PATH="$HOME/.ssh/id_ed25519"
if [ -f "$KEY_PATH" ]; then
    ssh-keygen -Y sign -f "$KEY_PATH" -n file "$OUTPUT_FILE" 2>/dev/null && \
    echo "[+] Termux ED25519 Signature attached: $SIG_FILE"
fi
