import subprocess
import os

print("[RUNTIME RESOLUTION] Deploying C# execution wrapper via available dotnet host...")

if os.path.exists("run_trihash.csx"):
    # Convert the C# script into a standalone console app so 'dotnet run' can compile and execute it natively
    if not os.path.exists("Program.cs"):
        subprocess.run(["dotnet", "new", "console", "--force"], check=True)
        
    with open("run_trihash.csx", "r") as f:
        csx_content = f.read()

    # Strip out #r directives that cause compiler errors in standard console apps
    clean_code = "\n".join([line for line in csx_content.splitlines() if not line.startswith("#r")])

    with open("Program.cs", "w") as f:
        f.write(clean_code)

    print("[+] Converted CSX script to Program.cs. Executing via dotnet run...")
    subprocess.run(["dotnet", "run"], check=True)
else:
    print("[-] Error: run_trihash.csx not found.")
