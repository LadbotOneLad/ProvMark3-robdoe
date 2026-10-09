#!/bin/bash
# Termux Sovereign Daemon Integration under NEVER DELETE, ONLY ABSORB

echo "[*] Initializing Termux Sovereign Wake-Lock & Daemon Service..."

# Ensure Termux API / wake lock tools are acknowledged
if command -v termux-wake-lock &> /dev/null; then
    termux-wake-lock
    echo "[+] Termux wake-lock acquired. CPU will remain active for sovereign pulse cycles."
else
    echo "[!] termux-wake-lock not found. Running in standard process space."
fi

# Execute continuous sovereign pulse loop
while true; do
    echo "[*] Executing scheduled sovereign heartbeat pulse..."
    python3 sovereign_heartbeat_pulse.py
    python3 sovereign_dashboard.py
    python3 sovereign_audit.py
    python3 sovereign_calendar_deck.py
    
    echo "[*] Pulse cycle complete. Sleeping for 3600 seconds..."
    sleep 3600
done
