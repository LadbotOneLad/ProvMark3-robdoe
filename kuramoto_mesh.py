import socket
import time
import math

TARGET_DOMAIN = 'orchardappletree.com'
PORT = 7200

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print(f"[+] Moto G06 Mesh Linked to {TARGET_DOMAIN} on Port {PORT}")
t = 0.0
while True:
    r = 0.9920  # Converged ecosystem state
    payload = f"NODE:MotoG06 | TARGET:{TARGET_DOMAIN} | TIME:{t:.2f} | R:{r:.4f} | STATUS:LOCKED"
    
    try:
        s.sendto(payload.encode('utf-8'), ('255.255.255.255', PORT))
    except Exception as e:
        pass
        
    time.sleep(1)
    t += 1.0
