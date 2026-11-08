def resolution_agent(state):
    state.recommended_action = (
        'auto_approve' if state.extracted_invoice and state.matched_po
        and state.extraction_confidence >= 0.85 and not state.discrepancies
        else 'flag_for_review'
    )
    state.agent_reasoning = (state.agent_reasoning or '') + ' | ' + (
        'PO matched; validation passed' if state.recommended_action == 'auto_approve'
        else 'Manual review required; inspect discrepancies'
    )
    return state
