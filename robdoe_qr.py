import hashlib

def generate_digital_soul():
    namespace = "robdoe.com"
    witness = "0xf091867EC603A6628eD83D274E8335539D82e9cc8"
    root_hash = "02da8df9d6bc0c1b23543f234df177db7c2237d462125b940c842d448f9af851"
    
    # Create a pseudo-matrix digital grid pattern based on the hash
    h_bytes = bytes.fromhex(root_hash[:32])
    
    print("================================================================")
    print("         ROBDOE.COM // 21ST CENTURY DIGITAL SOUL QR             ")
    print("================================================================")
    print(f"[*] Namespace : {namespace}")
    print(f"[*] Witness   : {witness}")
    print(f"[*] Root Hash : {root_hash}")
    print("----------------------------------------------------------------")
    print("               [ MATRIX-LATTICE VISUALIZER ]                    ")
    
    # Render an old-school ASCII matrix grid
    for i in range(8):
        row_str = ""
        for j in range(16):
            val = h_bytes[(i * 16 + j) % len(h_bytes)]
            row_str += "██" if (val % 2 == 0) else "  "
        print(f"    {row_str}  [{i}]")
        
    print("----------------------------------------------------------------")
    print("[+] Status: IMMUTABLE // FORWARD-ONLY // SOVEREIGN LOCK ACTIVE")
    print("================================================================")

if __name__ == "__main__":
    generate_digital_soul()
