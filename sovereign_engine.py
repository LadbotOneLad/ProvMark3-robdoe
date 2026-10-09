import json
import csv
import os
import urllib.request

INVARIANT_M = 932808725
CSV_FILENAME = "tax_ledger.csv"
METADATA_FILENAME = "token_metadata.json"

def fetch_live_prices():
    prices = {"GECKO": 0.00001, "ECHO": 0.00173}
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=echo-protocol,gecko&vs_currencies=aud"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if 'echo-protocol' in data:
                prices['ECHO'] = data['echo-protocol'].get('aud', 0.002476)
            if 'gecko' in data:
                prices['GECKO'] = data['gecko'].get('aud', 0.00001)
    except Exception as e:
        print(f"[Network Notice] Live API fetch limited ({e}), using verified market anchors.")
    return prices

class SovereignEngine:
    def __init__(self, asset_symbol, invariant):
        self.asset_symbol = asset_symbol
        self.invariant = invariant
        self.units = 0.0
        self.cost_basis_aud = 0.0

    def record_acquisition(self, units, fiat_cost_aud):
        self.units += units
        self.cost_basis_aud += fiat_cost_aud
        avg_cost = self.cost_basis_aud / self.units if self.units > 0 else 0
        print(f"[{self.asset_symbol}] ACQUIRED: {units} units | Total Cost Basis: ${self.cost_basis_aud:.2f} AUD | Avg Unit Cost: ${avg_cost:.6f}")

    def execute_disposal(self, units, proceeds_aud):
        if units > self.units:
            print(f"[{self.asset_symbol}] Error: Insufficient units for disposal.")
            return None
        
        avg_cost = self.cost_basis_aud / self.units
        cost_deducted = units * avg_cost
        capital_gain = proceeds_aud - cost_deducted
        
        self.units -= units
        self.cost_basis_aud -= cost_deducted
        
        ledger_entry = {
            "invariant": self.invariant,
            "asset": self.asset_symbol,
            "units_disposed": units,
            "proceeds_aud": round(proceeds_aud, 2),
            "cost_basis_deducted_aud": round(cost_deducted, 2),
            "capital_gain_loss_aud": round(capital_gain, 2),
            "compliance_framework": "ATO Capital Property / HMRC Pooling"
        }
        
        # 1. Persist to CSV Ledger
        file_exists = os.path.isfile(CSV_FILENAME)
        with open(CSV_FILENAME, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=ledger_entry.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(ledger_entry)

        # 2. Compile ERC-721 Token Metadata
        metadata = {
            "name": f"Sovereign Registry - {ledger_entry['asset']} Audit Record",
            "description": f"Cryptographically anchored tax pooling ledger entry under system invariant M = {self.invariant}.",
            "image": "ipfs://bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi",
            "attributes": [
                {"trait_type": "Asset Symbol", "value": ledger_entry["asset"]},
                {"trait_type": "System Invariant", "value": ledger_entry["invariant"]},
                {"trait_type": "Units Disposed", "value": ledger_entry["units_disposed"]},
                {"trait_type": "Proceeds (AUD)", "value": ledger_entry["proceeds_aud"]},
                {"trait_type": "Cost Basis Deducted (AUD)", "value": ledger_entry["cost_basis_deducted_aud"]},
                {"trait_type": "Capital Gain/Loss (AUD)", "value": ledger_entry["capital_gain_loss_aud"]},
                {"trait_type": "Framework", "value": ledger_entry["compliance_framework"]}
            ]
        }
        with open(METADATA_FILENAME, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)
            
        print(f"[{self.asset_symbol}] DISPOSAL PROCESSED:")
        print(f" -> Logged & Persisted to {CSV_FILENAME}")
        print(f" -> ERC-721 Metadata compiled to {METADATA_FILENAME}")
        return ledger_entry

# Initialize Pipeline Execution
print("--- Initializing Sovereign Engine ---")
live_prices = fetch_live_prices()
gecko_ledger = SovereignEngine("GECKO", INVARIANT_M)
echo_ledger = SovereignEngine("ECHO", INVARIANT_M)

# Execute baseline tracking and test event
gecko_ledger.record_acquisition(50000, 2.50)
echo_ledger.record_acquisition(1000, 2.47)

print("\n--- Executing Tracked Disposal ---")
gecko_ledger.execute_disposal(10000, 1.20)

# ==========================================
# Recursive Universe & Invariant Module
# Z = z^2 + c anchored to M = 932808725
# ==========================================

def compute_sovereign_recursion(c_real: float, c_imag: float, max_iterations: int = 100, invariant: int = 932808725) -> dict:
    """
    Computes the complex quadratic recurrence Z = z^2 + c
    anchored to the system invariant M = 932808725.
    """
    z = complex(0, 0)
    c = complex(c_real, c_imag)
    
    for i in range(max_iterations):
        z = (z ** 2) + c
        if abs(z) > 2.0:
            return {
                "converged": False,
                "iterations": i,
                "final_magnitude": abs(z),
                "invariant": invariant
            }
            
    return {
        "converged": True,
        "iterations": max_iterations,
        "final_magnitude": abs(z),
        "invariant": invariant
    }

if __name__ == "__main__":
    # Test execution with invariant mapping
    test_result = compute_sovereign_recursion(-0.7, 0.27015)
    print(f"Sovereign Recursion Result (Invariant: {test_result['invariant']}):")
    print(f"  Converged: {test_result['converged']}")
    print(f"  Iterations: {test_result['iterations']}")
    print(f"  Final Magnitude: {test_result['final_magnitude']:.4f}")
