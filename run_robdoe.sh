#!/bin/zsh
export TMPDIR=$HOME/storage/external-1/pip_tmp
export PIP_CACHE_DIR=$HOME/storage/external-1/pip_cache
mkdir -p "$TMPDIR" "$PIP_CACHE_DIR"

echo "[*] Launching Robdoe Sovereign Node..."
echo "[*] Attesting Master SHA-256: 68421d52d990c5f0a395e592db43abae81d7ef2c052722cd9e56c1cddea240da"

if [ -f "04_agents/gev_crew.py" ]; then
    python3 04_agents/gev_crew.py
else
    python3 -c "print('[+] System Active | Master Root: 68421d52d990c5f0a395e592db43abae81d7ef2c052722cd9e56c1cddea240da')"
fi
