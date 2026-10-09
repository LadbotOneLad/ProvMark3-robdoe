#!/usr/bin/env python3
import subprocess
import socket
import json

def get_network_info():
    print("================================================================")
    print("          TERMUX NETWORK & IP CONNECTIVITY DIAGNOSTICS          ")
    print("================================================================")
    
    # 1. Gather local network interfaces (ip addr)
    try:
        ip_addr_out = subprocess.check_output(["ip", "addr"], text=True)
        print("[+] Local Network Interfaces:")
        for line in ip_addr_out.splitlines():
            if "inet " in line or "inet6 " in line or "state UP" in line:
                print(f"    {line.strip()}")
    except Exception as e:
        print(f"[!] Could not run 'ip addr': {e}")
        
    # 2. Get hostname and primary IP
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"\n[+] Hostname: {hostname}")
        print(f"[+] Resolved Local IP: {local_ip}")
    except Exception:
        pass

    # 3. Check active listening ports (Ollama, SSH, etc.)
    print("\n[*] Checking active listening sockets/ports...")
    try:
        netstat_out = subprocess.check_output(["ss", "-tulpn"], text=True)
        for line in netstat_out.splitlines():
            if "LISTEN" in line or "ollama" in line or "python" in line:
                print(f"    {line.strip()}")
    except Exception:
        try:
            # Fallback to netstat if ss is unavailable
            netstat_out = subprocess.check_output(["netstat", "-tuln"], text=True)
            print(netstat_out)
        except Exception:
            print("    [!] Port inspection tools unavailable.")

    print("================================================================")
    print("CONNECTION METHODS:")
    print(" 1. Local Network (LAN): Connect using your phone's Wi-Fi IP address on port 11434.")
    print(" 2. Port Forwarding: Use SSH tunneling if connecting remotely (e.g., ssh -R ...)")
    print("================================================================")

if __name__ == "__main__":
    get_network_info()
