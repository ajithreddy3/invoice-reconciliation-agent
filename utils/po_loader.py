import json
from pathlib import Path

PO_PATH = Path(__file__).resolve().parents[1] / 'data' / 'purchase_orders.json'


def load_purchase_orders():
    with PO_PATH.open(encoding='utf-8') as stream:
        data = json.load(stream)
    if isinstance(data, dict) and 'purchase_orders' in data:
        return data['purchase_orders']
    if isinstance(data, list):
        return data
    raise ValueError('Invalid purchase_orders.json format')
