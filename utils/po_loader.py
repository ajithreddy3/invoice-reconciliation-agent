import json

def load_purchase_orders():
    """
    Always returns a LIST of purchase orders,
    regardless of JSON structure.
    """
    with open("data/purchase_orders.json", "r") as f:
        data = json.load(f)

    # Handle both formats safely
    if isinstance(data, dict) and "purchase_orders" in data:
        return data["purchase_orders"]

    if isinstance(data, list):
        return data

    raise ValueError("Invalid purchase_orders.json format")
