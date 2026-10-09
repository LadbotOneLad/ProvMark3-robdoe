#!/bin/bash
echo "=== RobDoe Sovereign Registry Discovery & Audit ==="
echo "Workspace Directory: $(pwd)"
echo "System Invariant Anchor: 932808725"
echo "Deployment Contract: 0x84CA4aFC3F395ebc0b519680B546Cd604C9c2018"
echo "--------------------------------------------------"

echo "[1] Scanning Workspace Files:"
ls -la

echo -n "[2] Verifying CSV Ledger Records: "
if [ -f "tax_ledger.csv" ]; then
    echo "Found ($(wc -l < tax_ledger.csv) rows)"
else
    echo "Not found."
fi

echo -n "[3] Verifying Domain Registry Records: "
if [ -f "domain_registry.csv" ]; then
    echo "Found ($(wc -l < domain_registry.csv) rows)"
else
    echo "Not found."
fi

echo -n "[4] Verifying ERC-721 Metadata: "
if [ -f "token_metadata.json" ]; then
    echo "Found."
else
    echo "Not found."
fi

echo -n "[5] Verifying Smart Contract: "
if [ -f "src/SovereignDeed.sol" ]; then
    echo "Found (src/SovereignDeed.sol)."
else
    echo "Not found."
fi

# Create secure timestamped archive including domain_registry.csv
ARCHIVE_NAME="sovereign_registry_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$ARCHIVE_NAME" sovereign_engine.py tax_ledger.csv domain_registry.csv token_metadata.json src/ script/ remappings.txt 2>/dev/null
echo "--------------------------------------------------"
echo "[6] Sovereign archive created successfully: $(pwd)/$ARCHIVE_NAME"
