from utils.schemas import Discrepancy
from utils.pdf import extract_text_from_pdf
from utils.invoice_parser import parse_invoice


def document_agent(state):
    try:
        text = extract_text_from_pdf(state.filename)
        invoice, issues = parse_invoice(text)
        state.extracted_invoice = invoice
        state.extraction_confidence = 0.9 if not issues else 0.4
        state.agent_reasoning = 'Parsed invoice fields and line items from PDF contents'
        for issue in issues:
            state.discrepancies.append(Discrepancy(type='extraction_incomplete', severity='high', details=issue))
    except Exception as error:
        state.extraction_confidence = 0
        state.agent_reasoning = 'PDF extraction failed; manual review required'
        state.discrepancies.append(Discrepancy(type='extraction_failed', severity='high', details=str(error)))
    return state
