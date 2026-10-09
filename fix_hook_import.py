import os

hook_path = "sovereign_pre_push_hook.py"

if os.path.exists(hook_path):
    with open(hook_path, "r") as f:
        content = f.read()

    if "import os" not in content:
        with open(hook_path, "w") as f:
            f.write("import os\n" + content)
        print("[+] Patched missing import os in sovereign pre-push hook.")
    else:
        print("[*] import os already verified in pre-push hook.")
else:
    print(f"[!] Target script {hook_path} not found in current namespace context.")
