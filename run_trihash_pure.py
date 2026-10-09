import subprocess
import datetime
import hashlib
import os

print("[PYTHON NATIVE FALLBACK] Executing absolute sovereign tri-hash sealing directly via Python runtime...")

timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
commit_count = int(subprocess.check_output(["git", "rev-list", "--count", "HEAD"]).decode().strip())
head_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
genesis = 0xe14f9a8d
prime_mod = 1000000007

# 1. Repo mass hash (tracked files, directory-safe)
tracked = subprocess.check_output(["git", "ls-files"]).decode().strip()
files = [f for f in tracked.split('\n') if f]

repo_sha = hashlib.sha512()
for f in files:
    if os.path.isfile(f):
        try:
            with open(f, "rb") as file_obj:
                repo_sha.update(file_obj.read())
        except (PermissionError, IOError):
            pass
repo_hash = repo_sha.hexdigest()

# 2. Staged delta hash
delta_out = subprocess.check_output(["git", "diff", "--cached"]).decode('utf-8', errors='ignore')
delta_hash = hashlib.sha512(delta_out.encode()).hexdigest()

# 3. Ancestry hash (last 10 commits)
ancestry_out = subprocess.check_output(["git", "log", "-10", "--pretty=%H"]).decode('utf-8', errors='ignore')
ancestry_hash = hashlib.sha512(ancestry_out.encode()).hexdigest()

# 4. Fused tri-hash invariant
fused_payload = (repo_hash + delta_hash + ancestry_hash).encode()
fused = hashlib.sha512(fused_payload).hexdigest()
raw = fused[:32]

invariant = 0
for c in raw:
    invariant = (invariant * 16 + int(c, 16)) % prime_mod

tag_name = f"TRIHASH-SEAL-v{commit_count}.{invariant}"

proof_content = f"""=====================================================================
SOVEREIGN MASTER: TRI-HASH INVARIANT ATTESTATION (PYTHON RUNTIME)
=====================================================================
Timestamp (UTC): {timestamp}
Repo Hash:     {repo_hash}
Delta Hash:    {delta_hash}
Ancestry Hash: {ancestry_hash}
Fused Hash:    {fused}
Invariant:     {invariant} (mod {prime_mod})
=====================================================================
[THE LAW OF ABSORPTION]
- Never delete, only absorb. Every tracked file, delta, and commit lineage is permanently sealed.
=====================================================================
"""

with open("TRIHASH_PROOF_ATTESTATION.md", "w") as f:
    f.write(proof_content)

subprocess.run(["git", "add", "TRIHASH_PROOF_ATTESTATION.md"], check=True)
subprocess.run(["git", "commit", "-m", f"feat(proof): tri-hash invariant anchor [invariant:{invariant}]"], check=True)
subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Trihash Proof: Repo={repo_hash} Delta={delta_hash} Ancestry={ancestry_hash} Invariant={invariant} Prime={prime_mod}"], check=True)
subprocess.run(["git", "push", "origin", "master", "--tags"], check=True)

print(f"[+] TRIHASH PROOF LOCKED (PYTHON).")
print(f"[+] Invariant = {invariant}")
print(f"[+] Tag       = {tag_name}")
