import os
import hashlib
import json

PLEROMA_STATE_FILE = ".pleroma_fractal_state.json"
PROOF_FILE = "MERKLE_TREE_ROOT_PROOF.md"

def compute_mandelbrot_lattice(width=64, height=64, max_iter=64):
    """Computes a Mandelbrot fractal lattice using z = z^2 + c in pure Python for Termux sovereign compatibility."""
    x_vals = [-2.0 + i * (2.5 / (width - 1)) for i in range(width)]
    y_vals = [-1.25 + j * (2.5 / (height - 1)) for j in range(height)]
    
    lattice_data = bytearray()
    for y in y_vals:
        for x in x_vals:
            c = complex(x, y)
            z = complex(0, 0)
            iter_count = 0
            while abs(z) <= 2.0 and iter_count < max_iter:
                z = z*z + c
                iter_count += 1
            lattice_data.append(iter_count % 256)
            
    fractal_hash = hashlib.sha256(lattice_data).hexdigest()
    return fractal_hash

def absorb_pleroma_state():
    fractal_hash = compute_mandelbrot_lattice()
    print(f"[PLEROMA FRACTAL] z = z^2 + c recursive entropy hash: {fractal_hash}")
    
    state = {}
    if os.path.exists(PLEROMA_STATE_FILE):
        with open(PLEROMA_STATE_FILE, "r") as f:
            state = json.load(f)
            
    history = state.get("history", [])
    history.append(fractal_hash)
    
    new_state = {
        "equation": "z = z^2 + c",
        "manifold": "pleroma",
        "total_absorptions": len(history),
        "latest_fractal_hash": fractal_hash,
        "history": history
    }
    
    with open(PLEROMA_STATE_FILE, "w") as f:
        json.dump(new_state, f, indent=2)
        
    with open(PROOF_FILE, "a") as f:
        f.write(f"\n- Pleroma Fractal Absorption (`z = z^2 + c`): `{fractal_hash}`\n")
        
    print(f"[+] Pleroma manifold absorbed into state tree. Total cycles: {len(history)}")

if __name__ == "__main__":
    absorb_pleroma_state()
