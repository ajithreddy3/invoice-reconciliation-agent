from utils.po_loader import load_purchase_orders


def matching_agent(state):
    invoice = state.extracted_invoice
    if not invoice or state.extraction_confidence < 0.85:
        return state
    orders = load_purchase_orders()
    if invoice.po_reference:
        candidates = [po for po in orders if po.get('po_number') == invoice.po_reference]
    else:
        candidates = [po for po in orders if abs(po['total'] - invoice.total) < 0.02
                      and po.get('currency') == invoice.currency
                      and po.get('supplier', '').casefold() == invoice.supplier.casefold()]
    if len(candidates) == 1:
        state.matched_po = candidates[0]
        state.po_match_confidence = 1.0 if invoice.po_reference else 0.6
    return state
