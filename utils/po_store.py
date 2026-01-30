import json
from pathlib import Path

PO_PATH = Path("data/purchase_orders.json")


def load_purchase_orders() -> list[dict]:
    """
    Always returns a list of PO dicts.
    Works even if JSON is a dict or malformed.
    """
    with open(PO_PATH, "r") as f:
        data = json.load(f)

    # Case 1: already a list
    if isinstance(data, list):
        return data

    # Case 2: dict of PO_NUMBER -> PO_DATA
    if isinstance(data, dict):
        return list(data.values())

    # Fallback
    return []
