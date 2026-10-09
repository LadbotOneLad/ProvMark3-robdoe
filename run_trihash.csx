#r "System.Runtime"
#r "System.IO.FileSystem"
#r "System.Security.Cryptography"

using System;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text;

Console.WriteLine("[.NET SCRIPT TRIHASH] Initializing directory-safe C# interactive sovereign sealing matrix...");

const string branch = "master";
const long prime = 1000000007;

string Run(string cmd)
{
    var psi = new ProcessStartInfo
    {
        FileName = "bash",
        Arguments = $"-lc \"{cmd}\"",
        RedirectStandardOutput = true,
        RedirectStandardError = true,
        UseShellExecute = false
    };
    using var p = Process.Start(psi);
    string output = p.StandardOutput.ReadToEnd();
    string err = p.StandardError.ReadToEnd();
    p.WaitForExit();
    if (p.ExitCode != 0 && !string.IsNullOrEmpty(err) && !err.Contains("Everything up-to-date"))
        throw new Exception(err);
    return output;
}

string Sha512Hex(string input)
{
    using var sha = SHA512.Create();
    byte[] data = Encoding.UTF8.GetBytes(input);
    return BitConverter.ToString(sha.ComputeHash(data)).Replace("-", "").ToLowerInvariant();
}

long ModHex(string hex, long prime)
{
    long value = 0;
    foreach (char c in hex)
    {
        int v = Convert.ToInt32(c.ToString(), 16);
        value = (value * 16 + v) % prime;
    }
    return value;
}

string tracked = Run("git ls-files");
string[] files = tracked.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);

using var shaMass = SHA512.Create();
foreach (var file in files)
{
    if (File.Exists(file))
    {
        try
        {
            byte[] data = File.ReadAllBytes(file);
            shaMass.TransformBlock(data, 0, data.Length, null, 0);
        }
        catch (Exception) { /* Skip non-files / directories gracefully */ }
    }
}
shaMass.TransformFinalBlock(Array.Empty<byte>(), 0, 0);
string repoHash = BitConverter.ToString(shaMass.Hash).Replace("-", "").ToLowerInvariant();

string deltaHash = Sha512Hex(Run("git diff --cached"));
string ancestryHash = Sha512Hex(Run("git log -10 --pretty=%H"));

string fused = Sha512Hex(repoHash + deltaHash + ancestryHash);
string raw = fused.Substring(0, 32);
long invariant = ModHex(raw, prime);

string proofFile = "TRIHASH_PROOF_ATTESTATION.md";
File.WriteAllText(proofFile, $@"=====================================================================
SOVEREIGN MASTER: TRI-HASH INVARIANT ATTESTATION (.NET SCRIPT)
=====================================================================
- Branch: {branch}
- Repo Hash:     {repoHash}
- Delta Hash:    {deltaHash}
- Ancestry Hash: {ancestryHash}
- Fused Hash:    {fused}
- Invariant:     {invariant} (mod {prime})
=====================================================================
[THE LAW OF ABSORPTION]
- Never delete, only absorb. Every file, delta, and commit is sealed.
=====================================================================
");

Run($"git add {proofFile}");
Run($"git commit -m \"feat(proof): tri-hash invariant anchor [invariant:{invariant}]\"");

string count = Run("git rev-list --count HEAD").Trim();
string tag = $"TRIHASH-SEAL-v{count}.{invariant}";

Run($"git tag -a {tag} -m \"Trihash Proof: Repo={repoHash} Delta={deltaHash} Ancestry={ancestryHash} Invariant={invariant} Prime={prime}\"");
Run($"git push origin {branch} --tags");

Console.WriteLine("[+] TRIHASH PROOF LOCKED (.NET SCRIPT).");
Console.WriteLine($"[+] Invariant = {invariant}");
Console.WriteLine($"[+] Tag       = {tag}");
