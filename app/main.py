import json
from app.graph import app
from utils.schemas import AgentState

def serialize(obj):
    """
    Recursively serialize Pydantic models into dicts
    so json.dumps never crashes.
    """
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize(i) for i in obj]
    return obj


def main():
    invoices = [
        "data/invoices/Invoice_1_Baseline.pdf",
        "data/invoices/Invoice_2_Scanned.pdf",
        "data/invoices/Invoice_3_Different_Format.pdf",
        "data/invoices/Invoice_4_Price_Trap.pdf",
        "data/invoices/Invoice_5_Missing_PO.pdf",
    ]

    for invoice_path in invoices:
        print(f"\n=== Processing {invoice_path} ===\n")

        state = AgentState(filename=invoice_path)
        result = app.invoke(state)

        safe_result = serialize(result)
        print(json.dumps(safe_result, indent=2))


if __name__ == "__main__":
    main()
