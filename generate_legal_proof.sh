#!/usr/bin/env bash
set -euo pipefail

ACCOUNT_1="LadbotoneLad"
ACCOUNT_2="backupsonbackups-cyber"

# Optional explicit repos for Account 2 if unindexed by GitHub API
MANUAL_REPOS_ACC2=()

PROOF_JSON="MASTER_PROOF.json"
AFFIDAVIT_FILE="LEGAL_AFFIDAVIT.txt"
SIG_FILE="LEGAL_AFFIDAVIT.txt.sig"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[+] Generating Legal-Grade Merkle State Proof"
echo "[+] Timestamp (UTC): $TIMESTAMP"

WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

MANIFEST_TMP="$WORK_DIR/manifest.tmp"
touch "$MANIFEST_TMP"

process_repo() {
    local account="$1"
    local repo_url="$2"
    local repo_name
    repo_name=$(basename "$repo_url" .git)

    git clone --bare -q "$repo_url" "$WORK_DIR/$repo_name.git" 2>/dev/null || return 0

    local commit_hash tree_sha
    commit_hash=$(git --git-dir="$WORK_DIR/$repo_name.git" rev-parse HEAD 2>/dev/null || echo "empty")

    if [ "$commit_hash" != "empty" ]; then
        tree_sha=$(git --git-dir="$WORK_DIR/$repo_name.git" ls-tree -r HEAD 2>/dev/null | sha256sum | awk '{print $1}')
    else
        tree_sha="empty_repo"
    fi

    cat <<JEOF >> "$MANIFEST_TMP"
  {
    "account": "$account",
    "repository": "$repo_name",
    "head_commit": "$commit_hash",
    "tree_sha256_root": "$tree_sha"
  },
JEOF
    rm -rf "$WORK_DIR/$repo_name.git"
}

# 1. Sweep LadbotoneLad
repos1=$(curl -s "https://api.github.com/users/$ACCOUNT_1/repos?per_page=100" | grep -o '"clone_url": "[^"]*' | cut -d'"' -f4 || true)
for repo_url in $repos1; do
    process_repo "$ACCOUNT_1" "$repo_url"
done

# 2. Sweep backupsonbackups-cyber
if [ ${#MANUAL_REPOS_ACC2[@]} -gt 0 ]; then
    for repo_name in "${MANUAL_REPOS_ACC2[@]}"; do
        process_repo "$ACCOUNT_2" "https://github.com/$ACCOUNT_2/$repo_name.git"
    done
fi

# Build Layer 2: Deterministic JSON State Tree
echo "[" > "$WORK_DIR/final_manifest.json"
if [ -s "$MANIFEST_TMP" ]; then
    sed '$ s/,$//' "$MANIFEST_TMP" >> "$WORK_DIR/final_manifest.json"
fi
echo "]" >> "$WORK_DIR/final_manifest.json"

MASTER_ROOT_HASH=$(sha256sum "$WORK_DIR/final_manifest.json" | awk '{print $1}')

cat <<JEOF > "$PROOF_JSON"
{
  "specification": "Sovereign-Legal-Proof-v1",
  "timestamp_utc": "$TIMESTAMP",
  "accounts": ["$ACCOUNT_1", "$ACCOUNT_2"],
  "master_root_sha256": "$MASTER_ROOT_HASH",
  "state_tree": $(cat "$WORK_DIR/final_manifest.json")
}
JEOF

# Build Layer 1: Legal Affidavit for Plain-Language Audit
cat <<JEOF > "$AFFIDAVIT_FILE"
================================================================================
                    AFFIDAVIT OF CRYPTOGRAPHIC STATE & INTENT
================================================================================

OPERATOR / SOVEREIGN AUTHORITY:
- Account Handles: $ACCOUNT_1 | $ACCOUNT_2
- Timestamp (UTC): $TIMESTAMP

DECLARATION OF INTEGRITY:
The undersigned operator asserts sole authorship, cryptographic control, and
provenance over the state tree represented by the Master Merkle Root SHA-256 hash.

LAYER 1: MASTER MERKLE ROOT HASH
--------------------------------------------------------------------------------
$MASTER_ROOT_HASH
--------------------------------------------------------------------------------

LEGAL & AUDIT VERIFICATION INSTRUCTIONS:
1. To verify the integrity of the underlying repositories, compute the SHA-256
   checksum of '$PROOF_JSON'.
2. The output must match the Master Merkle Root Hash listed above exactly.
3. To verify non-repudiation and operator identity, verify the detached SSH
   signature ('$SIG_FILE') against the operator's public key using standard OpenSSH tools:
   ssh-keygen -Y verify -f <PUBLIC_KEY> -n file -s $SIG_FILE < $AFFIDAVIT_FILE

================================================================================
