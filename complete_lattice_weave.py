import os
import subprocess
import hashlib
import json
import time

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=False)

def main():
    print("================================================================================")
    print("      SETTLEMENT-VECTOR LATTICE WEAVE (NEMOSIS INTEGRATED)")
    print("================================================================================")
    
    repos = {
        "GLOBAL_REGISTERY": "https://github.com/robdoeAiagency101/GLOBAL_REGISTERY.git",
        "AiAgency.101-MagnaCarta": "https://github.com/AiTenetAgency101/AiAgency.101-MagnaCarta.git",
        "zhangxuefeng-skill": "https://github.com/alchaincyf/zhangxuefeng-skill.git",
        "spacewasm": "https://github.com/nasa/spacewasm.git",
        "T800-AiGC": "https://github.com/AiAgency-Lab/T800-AiGC.git",
        "MP-SPDZ": "https://github.com/data61/MP-SPDZ.git",
        "atmospheric-truth-layer": "https://github.com/AiTenetAgency101/atmospheric-truth-layer.git",
        "panodata-map-panel": "https://github.com/backupsonbackupsrobby-cyber/panodata-map-panel.git",
        "kuramoto": "https://github.com/fabridamicelli/kuramoto.git",
        "The-Ai-Whispher": "https://github.com/backupsonbackupsrobby-cyber/The-Ai-Whispher.git",
        "PowerShell-Fkn-RobDoing": "https://github.com/backupsonbackupsrobby-cyber/PowerShell-Fkn-RobDoing.git",
        "bureau_of_meteorology": "https://github.com/backupsonbackupsrobby-cyber/bureau_of_meteorology.git",
        "chrome-devtools-mcp": "https://github.com/backupsonbackupsrobby-cyber/chrome-devtools-mcp.git",
        "opennem": "https://github.com/backupsonbackupsrobby-cyber/opennem.git",
        "NEMSEER": "https://github.com/robdoeAiagency101/NEMSEER.git",
        "NEMOSIS": "https://github.com/backupsonbackupsrobby-cyber/NEMOSIS.git"
    }
    
    workspace = os.getcwd()
    print(f"Active Workspace: {workspace}")
    
    for name, url in repos.items():
        repo_path = os.path.join(workspace, name)
        if not os.path.exists(repo_path):
            print(f"Cloning settlement node: {name}...")
            run_cmd(f"git clone {url}")
        else:
            print(f"Repository {name} already present in mesh.")

    # Ngāpuhi Whare structural anchor hash
    ngapuhi_whare_hash = "3185e432d4ed6591c341556e6de9811bbdbace95d9d570f165990511616d491dca8bdfeb3e0398588662b635bad339c53ef2395a595c065477b5e6b6ac7817ef"
    
    accumulator = ngapuhi_whare_hash.encode()
    total_files = 0
    file_inventory = []
    
    for name in repos.keys():
        repo_path = os.path.join(workspace, name)
        if os.path.exists(repo_path):
            print(f"Binding nodes in: {name}")
            for root, dirs, files in os.walk(repo_path):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in sorted(files):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, workspace)
                    try:
                        with open(file_path, "rb") as f:
                            f_content = f.read()
                            f_hash = hashlib.sha256(f_content).hexdigest()
                        accumulator = hashlib.sha512(accumulator + f_hash.encode()).digest()
                        total_files += 1
                        file_inventory.append(rel_path)
                    except Exception:
                        pass
        else:
            accumulator = hashlib.sha512(accumulator + name.encode()).digest()

    master_lattice_root = hashlib.sha512(accumulator).hexdigest()
    
    manifest = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000000+00:00"),
        "lineage": "Te Whare o Ngāpuhi",
        "axis": "Whīria & Te Toka Tū Moana (NEMOSIS Settlement Simulation Extension)",
        "leaf_nodes": "Kooris Active (Nomadic Mesh)",
        "synchronized_repositories": list(repos.keys()),
        "total_artifacts_bound": total_files,
        "master_lattice_root": master_lattice_root
    }
    
    with open("master_lattice_manifest.json", "w") as out:
        json.dump(manifest, out, indent=4)
        
    print("================================================================================")
    print(f"SYNCHRONIZATION COMPLETE: {total_files} artifact nodes bound across all repos.")
    print(f"MANIFEST updated: master_lattice_manifest.json")
    print(f"SETTLEMENT-VECTOR MASTER LATTICE MERKLE ROOT:\n{master_lattice_root}")
    print("================================================================================")

if __name__ == "__main__":
    main()
