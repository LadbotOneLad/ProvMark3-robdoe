import json

registry_state = {
    "invariant": 932808725,
    "assets": {
        "gecko": {"network": "Solana/Base", "tracking": "Active"},
        "echo": {"network": "MoveVM / Bitcoin Restaking", "tracking": "Active"}
    },
    "compliance": "AU-ATO / UK-HMRC Property Pooling Enabled"
}

print(json.dumps(registry_state, indent=4))
