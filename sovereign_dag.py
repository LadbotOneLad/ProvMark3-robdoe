import hashlib

invariant = "932808725"
print(f"Loading RobDoe Sovereign Registry under invariant M = {invariant}")
print("DAG Root Hash: " + hashlib.sha256(invariant.encode()).hexdigest())
