from utils.schemas import Discrepancy

def discrepancy_agent(state):
    invoice = state.extracted_invoice
    po = state.matched_po

    if not po:
        state.discrepancies.append(
            Discrepancy(
                type="no_matching_po",
                severity="high",
                details="No purchase order could be confidently matched",
                invoice_total=invoice.total
            )
        )
        return state

    variance = ((invoice.total - po["total"]) / po["total"]) * 100

    if abs(variance) > 5:
        state.discrepancies.append(
            Discrepancy(
                type="price_mismatch",
                severity="high",
                details="Invoice total deviates significantly from PO",
                invoice_total=invoice.total,
                po_total=po["total"],
                variance_percentage=round(variance, 2)
            )
        )

    return state
