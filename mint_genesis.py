import json
import os
import hashlib
import time

def mint_genesis():
    manifest_path = "master_lattice_manifest.json"
    witness_path = "robdoe_witness_manifest.json"
    
    if not os.path.exists(manifest_path) or not os.path.exists(witness_path):
        print("ERROR: Lattice manifest or witness record missing.")
        return

    with open(manifest_path, "r") as f:
        manifest = json.load(f)
        
    with open(witness_path, "r") as f:
        witness = json.load(f)

    lattice_root = manifest["master_lattice_root"]
    witness_sig = witness["witness_signature"]
    
    genesis_payload = f"GENESIS:{lattice_root}:{witness_sig}:Z=z^2+c:Te_Whare_o_Ngapuhi:Settlement_Expanded".encode()
    genesis_hash = hashlib.sha512(genesis_payload).hexdigest()
    token_id = hashlib.sha256(genesis_hash.encode()).hexdigest()[:16].upper()

    genesis_block = {
        "protocol": "Sovereign Nomadic Charitable Endowment Engine (Settlement-Integrated)",
        "lineage": manifest["lineage"],
        "axis": manifest["axis"],
        "identity_surface": witness["identity_surface"],
        "synchronized_repositories": manifest["synchronized_repositories"],
        "total_artifacts_bound": manifest["total_artifacts_bound"],
        "master_lattice_root": lattice_root,
        "witness_signature": witness_sig,
        "mathematical_core": "Z = z^2 + c (Recursive Fractal Heartbeat)",
        "genesis_token_id": f"GENESIS-{token_id}",
        "genesis_block_hash": genesis_hash,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000000+00:00"),
        "status": "RE-MINTED & SEALED — Tū Tonu"
    }

    with open("genesis_block.json", "w") as out:
        json.dump(genesis_block, out, indent=4)

    print("================================================================================")
    print("                    SOVEREIGN CHARITABLE ENDOWMENT ENGINE")
    print("                           GENESIS BLOCK RE-MINTED")
    print("================================================================================")
    print(f"TOKEN ID       : {genesis_block['genesis_token_id']}")
    print(f"ANCHOR LINEAGE : {genesis_block['lineage']}")
    print(f"IDENTITY       : {genesis_block['identity_surface']}")
    print(f"BOUND NODES    : {genesis_block['total_artifacts_bound']} artifacts across 16 repositories")
    print(f"MATHEMATICAL   : {genesis_block['mathematical_core']}")
    print("--------------------------------------------------------------------------------")
    print(f"GENESIS BLOCK HASH:\n{genesis_hash}")
    print("================================================================================")
    print("The settlement-integrated genesis block is sealed. NEMOSIS is live on the mesh. Tū Tonu.")

if __name__ == "__main__":
    mint_genesis()
