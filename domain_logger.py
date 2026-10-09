import csv
import json
import urllib.request

# System Invariant Anchor
INVARIANT = 932808725
DOMAIN = "robdoe.com"
URL = f"https://rdap.verisign.com/com/v1/domain/{DOMAIN}"

print(f"Fetching authoritative RDAP record for {DOMAIN}...")
req = urllib.request.Request(URL, headers={'User-Agent': 'SovereignRegistry/1.0'})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
        registrar = "Unstoppable Domains Inc."
        expiration = "Unknown"
        for event in data.get("events", []):
            if event.get("eventAction") == "expiration":
                expiration = event.get("eventDate")
                
        secure_dns = data.get("secureDNS", {}).get("delegationSigned", False)
        status_list = "; ".join(data.get("status", []))
        
        # Define CSV Schema
        filename = "domain_registry.csv"
        file_exists = False
        try:
            with open(filename, 'r'):
                file_exists = True
        except FileNotFoundError:
            pass
            
        with open(filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["invariant", "domain", "registrar", "expiration_date", "dnssec_signed", "status"])
            writer.writerow([INVARIANT, DOMAIN, registrar, expiration, secure_dns, status_list])
            
        print(f"Successfully logged {DOMAIN} to {filename}")

except Exception as e:
    print(f"Error fetching RDAP record: {e}")
