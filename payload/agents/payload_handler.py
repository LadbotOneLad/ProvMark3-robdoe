import json

def load_payload():
    with open("payload/state/lattice_payload.json", "r") as f:
        data = json.load(f)
    print(f"[*] CrewAI Payload Loaded: {data['payload_id']}")
    print(f"[*] State Vector Verified: {len(data['state_vector'])} nodes active.")
    return data

if __name__ == "__main__":
    load_payload()
