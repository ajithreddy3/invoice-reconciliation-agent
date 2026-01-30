from pydantic import BaseModel
from typing import List, Optional

class LineItem(BaseModel):
    description: str
    quantity: float
    unit: str
    unit_price: float
    line_total: float
    extraction_confidence: float

class ExtractedInvoice(BaseModel):
    invoice_number: str
    invoice_date: str
    supplier: str
    po_reference: Optional[str]
    currency: str
    line_items: List[LineItem]
    subtotal: float
    vat: float
    total: float

class Discrepancy(BaseModel):
    type: str
    severity: str
    details: str
    invoice_total: Optional[float] = None
    po_total: Optional[float] = None
    variance_percentage: Optional[float] = None

class AgentState(BaseModel):
    filename: str
    extracted_invoice: Optional[ExtractedInvoice] = None
    matched_po: Optional[dict] = None
    discrepancies: List[Discrepancy] = []
    extraction_confidence: float = 0.0
    po_match_confidence: float = 0.0
    recommended_action: Optional[str] = None
    agent_reasoning: Optional[str] = None
