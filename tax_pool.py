import json
import requests

def get_live_fx_rate(base="GBP", target="AUD"):
    try:
        url = f"https://api.exchangerate.fun/latest?base={base}"
        response = requests.get(url, timeout=5)
        data = response.json()
        rate = data["rates"].get(target)
        if rate:
            return rate
    except Exception as e:
        print(f"[FX Warning] Could not fetch live rate ({e}), using fallback 1.90")
    return 1.90 # fallback rate if offline

class SovereignTaxPool:
    def __init__(self, asset_name, invariant, jurisdiction="AUD"):
        self.asset_name = asset_name
        self.invariant = invariant
        self.jurisdiction = jurisdiction # "AUD" (ATO) or "GBP" (HMRC)
        self.total_units = 0.0
        self.total_cost_basis = 0.0
        
        # Fetch conversion factor relative to jurisdiction preference
        self.fx_rate = get_live_fx_rate("GBP", "AUD")
        print(f"[{self.asset_name}] Initialized under {self.jurisdiction} mapping. Live GBP/AUD FX Rate: {self.fx_rate}")

    def convert_currency(self, amount, source_currency, target_currency):
        if source_currency == target_currency:
            return amount
        if source_currency == "GBP" and target_currency == "AUD":
            return amount * self.fx_rate
        if source_currency == "AUD" and target_currency == "GBP":
            return amount / self.fx_rate
        return amount

    def acquire(self, units, cost, currency="AUD"):
        # Normalize cost to system tracking currency
        normalized_cost = self.convert_currency(cost, currency, self.jurisdiction)
        self.total_units += units
        self.total_cost_basis += normalized_cost
        avg_cost = self.total_cost_basis / self.total_units if self.total_units > 0 else 0
        print(f"[{self.asset_name}] ACQUIRED: {units} units | Cost: {cost} {currency} ({normalized_cost:.2f} {self.jurisdiction}) | Avg Cost: {avg_cost:.4f}")

    def dispose(self, units, proceeds, currency="AUD"):
        if units > self.total_units:
            print(f"[{self.asset_name}] ERROR: Insufficient units in pool.")
            return None
        
        normalized_proceeds = self.convert_currency(proceeds, currency, self.jurisdiction)
        avg_cost = self.total_cost_basis / self.total_units
        cost_of_goods_sold = units * avg_cost
        capital_gain = normalized_proceeds - cost_of_goods_sold
        
        self.total_units -= units
        self.total_cost_basis -= cost_of_goods_sold
        
        result = {
            "asset": self.asset_name,
            "units_disposed": units,
            "proceeds_recorded": f"{normalized_proceeds:.2f} {self.jurisdiction}",
            "cost_basis_deducted": f"{cost_of_goods_sold:.2f} {self.jurisdiction}",
            "capital_gain_loss": f"{capital_gain:.2f} {self.jurisdiction}",
            "invariant_anchor": self.invariant,
            "tax_framework": "ATO (Australia)" if self.jurisdiction == "AUD" else "HMRC (UK)"
        }
        print(f"[{self.asset_name}] DISPOSAL: Gain/Loss: {capital_gain:.2f} {self.jurisdiction}")
        return result

# Execute demonstration tracking for GECKO mapped to Australian ATO (AUD)
print("--- Simulating ATO Compliance Stream (AUD) ---")
gecko_pool = SovereignTaxPool("GECKO", 932808725, jurisdiction="AUD")
gecko_pool.acquire(10000, 50.0, currency="AUD")
disposal_record = gecko_pool.dispose(2000, 15.0, currency="AUD")

print("\nCompliance Log Export:")
print(json.dumps(disposal_record, indent=4))
