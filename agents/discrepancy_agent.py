from utils.schemas import Discrepancy


def discrepancy_agent(state):
    invoice, po = state.extracted_invoice, state.matched_po
    if invoice is None:
        return state

    def flag(kind, details):
        state.discrepancies.append(Discrepancy(type=kind, severity='high', details=details, invoice_total=invoice.total))

    if not invoice.po_reference:
        flag('missing_po_reference', 'Invoice has no explicit PO reference; candidate match requires review')
    if not po:
        flag('no_matching_po', 'No unique purchase order could be matched')
        return state
    if invoice.currency != po.get('currency'):
        flag('currency_mismatch', 'Invoice currency differs from purchase order')
    if invoice.supplier.casefold() != po.get('supplier', '').casefold():
        flag('supplier_mismatch', 'Supplier names differ; manual verification required')
    if abs(invoice.total - po['total']) > 0.02:
        flag('total_mismatch', f"Invoice total {invoice.total} differs from PO total {po['total']}")
    matched = set()
    for item in invoice.line_items:
        candidates = [(index, row) for index, row in enumerate(po.get('line_items', []))
                      if row['description'].casefold() == item.description.casefold()]
        if len(candidates) != 1 or candidates[0][0] in matched:
            flag('line_item_mismatch', f'No unique PO line for {item.description}')
            continue
        index, row = candidates[0]
        matched.add(index)
        for key in ('quantity', 'unit_price', 'line_total'):
            if abs(getattr(item, key) - row[key]) > 0.02:
                flag('price_mismatch' if key != 'quantity' else 'quantity_mismatch', f'{item.description}: {key} differs from PO')
        if item.unit.casefold() != row.get('unit', '').casefold():
            flag('unit_mismatch', f'{item.description}: unit differs from PO')
    if len(matched) != len(po.get('line_items', [])):
        flag('line_item_mismatch', 'Not all PO lines were matched')
    return state
