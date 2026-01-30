from utils.po_loader import load_purchase_orders

def matching_agent(state):
    invoice = state.extracted_invoice
    purchase_orders = load_purchase_orders()

    # Safety check
    if not invoice or not purchase_orders:
        return state

    for po in purchase_orders:
        # Defensive: ensure po is dict
        if not isinstance(po, dict):
            continue

        # 1️⃣ STRONG MATCH — total amount
        if "total" in po and abs(po["total"] - invoice.total) < 1e-2:
            state.matched_po = po
            state.po_match_confidence = 1.0
            return state

        # 2️⃣ FALLBACK — line-item overlap
        po_items = po.get("line_items", [])
        if not po_items:
            continue

        matches = 0
        for inv_item in invoice.line_items:
            for po_item in po_items:
                if inv_item.description.lower() in po_item["description"].lower():
                    matches += 1

        if matches >= max(1, len(invoice.line_items) * 0.5):
            state.matched_po = po
            state.po_match_confidence = 0.6
            return state

    return state
