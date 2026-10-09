import json
import os

target_dir = "/data/data/com.termux/files/home/robdoerootauthority"
os.makedirs(target_dir, exist_ok=True)

manifest_path = os.path.join(target_dir, "workspace_manifest.json")
manifest = {
    "node_id": "robertu",
    "components": {
        "termux_automation": "termux_daemon_manager.py",
        "repo_hygiene": "repo_hygiene.py",
        "ai_bridge": "ollama_bridge_core.py"
    },
    "status": "Saved & Verified"
}

with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=4)

print(f"[+] Successfully wrote manifest to: {manifest_path}")
