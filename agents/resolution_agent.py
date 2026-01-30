def resolution_agent(state):
    if not state.discrepancies:
        state.recommended_action = "auto_approve"
    else:
        state.recommended_action = "flag_for_review"

    state.agent_reasoning += " | PO matched by total or line items"
    return state
