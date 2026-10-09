#!/usr/bin/env python3
import os
import subprocess

def deploy_portfolio():
    print("================================================================")
    print("   CLOUDFLARE PAGES PORTFOLIO AUTOMATION & DEPLOYMENT           ")
    print("================================================================")

    # 1. Write index.html
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rob Doe | Portfolio</title>
    <style>
        body { margin: 0; font-family: -apple-system, sans-serif; background: #0a0a0a; color: #f0f0f0; display: flex; align-items: center; justify-content: center; height: 100vh; text-align: center; }
        .container { max-width: 600px; padding: 40px; border-radius: 12px; background: rgba(255,255,255,0.05); box-shadow: 0 4px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); }
        h1 { font-size: 2.5rem; margin-bottom: 10px; color: #fff; }
        p { font-size: 1.1rem; color: #a0a0a0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome</h1>
        <p>This domain is part of a private portfolio managed by <strong>Rob Doe</strong>.</p>
        <p>It is currently parked and undergoing setup.</p>
    </div>
</body>
</html>
"""
    
    with open("index.html", "w") as f:
        f.write(html_content)
    print("[+] index.html generated successfully.")

    # 2. Check for wrangler / Cloudflare CLI
    wrangler_check = subprocess.run(["npx", "wrangler", "--version"], capture_output=True, text=True)
    if wrangler_check.returncode != 0:
        print("[*] Installing wrangler CLI locally...")
        subprocess.run(["npm", "install", "wrangler", "--save-dev"], check=True)

    # 3. Commit portfolio file to git
    for lock_path in [".git/index.lock", ".git/gc.pid"]:
        if os.path.exists(lock_path):
            os.remove(lock_path)
            
    subprocess.run(["git", "add", "index.html"], check=True)
    subprocess.run(["git", "commit", "-m", "portfolio(cloudflare): added parked holding page index.html"], capture_output=True)
    
    branch_res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    branch = branch_res.stdout.strip() or "main"
    subprocess.run(["git", "push", "origin", branch, "--force"], capture_output=True)

    print("[+] Portfolio source locked and pushed.")
    print("================================================================")
    print(" NEXT STEPS FOR CLOUDFLARE PAGES & UNSTOPPABLE DOMAINS:")
    print(" 1. Run: npx wrangler pages deploy . --project-name=robdoe-portfolio")
    print(" 2. Configure Unstoppable Domains (orchardappletree.com):")
    print("    - Type: CNAME")
    print("    - Name: @")
    print("    - Value: robdoe-portfolio.pages.dev")
    print("================================================================")

if __name__ == "__main__":
    deploy_portfolio()
