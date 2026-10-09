#!/usr/bin/env python3
import subprocess
import json

def get_wifi_ip():
    print("================================================================")
    print("           TERMUX ANDROID NETWORK CONFIGURATION                 ")
    print("================================================================")
    
    # Android provides network info via termux-wifi-connection or ifconfig
    try:
        ifconfig_out = subprocess.check_output(["ifconfig"], text=True)
        print("[+] Network Interfaces (ifconfig):")
        for line in ifconfig_out.splitlines():
            if "inet " in line or "UP" in line:
                print(f"    {line.strip()}")
    except Exception as e:
        print(f"[!] ifconfig failed: {e}")
        
    # Try querying Wi-Fi info via Termux API if installed
    try:
        wifi_info = subprocess.check_output(["termux-wifi-connectionInfo"], text=True)
        print(f"\n[+] Wi-Fi Connection Info:\n{wifi_info}")
    except Exception:
        print("\n[!] Termux-API not installed. To get detailed Wi-Fi state, run:")
        print("    pkg install termux-api")
        
    print("================================================================")
    print("To connect from another device on your local Wi-Fi:")
    print(" 1. Find your phone's Wi-Fi IP address from the output above (usually wlan0).")
    print(" 2. Ensure Ollama is bound to 0.0.0.0 (already configured).")
    print(" 3. Access via: http://<PHONE_WIFI_IP>:11434")
    print("================================================================")

if __name__ == "__main__":
    get_wifi_ip()
