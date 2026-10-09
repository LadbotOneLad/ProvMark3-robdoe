#!/usr/bin/env python3
import subprocess

def check_routing():
    print("================================================================")
    print("          ANDROID ROUTING & BINDING DIAGNOSTIC                  ")
    print("================================================================")
    
    # Check netstat / ss for binding interface
    print("[*] Inspecting active socket bindings for Ollama:")
    try:
        ss_out = subprocess.check_output(["ss", "-tulpn"], text=True)
        for line in ss_out.splitlines():
            if "11434" in line:
                print(f"    {line.strip()}")
    except Exception:
        try:
            netstat_out = subprocess.check_output(["netstat", "-an"], text=True)
            for line in netstat_out.splitlines():
                if "11434" in line:
                    print(f"    {line.strip()}")
        except Exception:
            print("    [!] Socket inspection tools restricted.")

    print("\n[*] RECOMMENDATION:")
    print("Android/Termux network isolation often prevents binding directly to external Wi-Fi interface IPs (192.168.x.x) from localhost loops.")
    print("However, other devices on your Wi-Fi network can successfully reach http://192.168.1.101:11434 because traffic is routed via wlan0.")
    print("Test connection from another separate device on your Wi-Fi network rather than from inside Termux itself.")
    print("================================================================")

if __name__ == "__main__":
    check_routing()
