"""Conservative parser for English invoices with quantity/unit/price/total rows."""
import re
from decimal import Decimal
from utils.schemas import ExtractedInvoice, LineItem

NUMBER = r'(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d{1,2})?'
MONEY = rf'[^\w\d\s]*\s*({NUMBER})'
CODE = r'\b[A-Z]{2,}(?:-[A-Z0-9]+)+\b'


def amount(value):
    return float(Decimal(value.replace(',', '')))


def parse_invoice(text):
    def field(pattern, default=''):
        match = re.search(pattern, text, re.I | re.M)
        return match.group(1).strip() if match else default

    items = []
    for line in text.splitlines():
        match = re.match(rf'^(.+?)\s+({NUMBER})\s+(kg|g|mg|l|ml|pcs?|units?|each|ea|hours?|hrs?)\s+{MONEY}\s+{MONEY}\s*$', line.strip(), re.I)
        if not match:
            continue
        description, quantity, unit, price, total = match.groups()
        description = re.sub(CODE, '', description).strip()
        items.append(LineItem(description=description, quantity=amount(quantity), unit=unit,
                              unit_price=amount(price), line_total=amount(total), extraction_confidence=0.9))

    def total_field(label):
        value = field(rf'^\s*(?:{label})\s*:?\s*{MONEY}\s*$')
        return amount(value) if value else None

    subtotal = total_field(r'subtotal|net amount|net total')
    vat = total_field(r'VAT(?:\s*\(\d+(?:\.\d+)?%\)|\s*@\s*\d+(?:\.\d+)?%)?|tax')
    total = total_field(r'grand total|total due|amount due|total')
    currency = field(r'\bcurrency\s*:\s*(GBP|USD|EUR)\b').upper()
    if not currency:
        currency = next((code for symbol, code in [('£', 'GBP'), ('€', 'EUR'), ('$', 'USD')] if symbol in text), 'UNKNOWN')
    if currency == 'UNKNOWN':
        currency = field(r'\b(GBP|USD|EUR)\s+\d', 'UNKNOWN').upper()
    invoice = ExtractedInvoice(
        invoice_number=field(r'^\s*(?:invoice\s*(?:number|no\.?|#)|no\.?)\s*:\s*(\S+)','UNKNOWN'),
        invoice_date=field(r'\binvoice\s*date\s*:\s*([^\n]+)') or field(r'^\s*date\s*:\s*([^\n]+)'),
        supplier=next((line.strip() for line in text.splitlines() if line.strip()), 'UNKNOWN'),
        po_reference=field(r'^\s*(?:PO\s*(?:reference|number|no\.?)|ref)\s*:\s*(PO-[\w-]+)', None),
        currency=currency, line_items=items, subtotal=subtotal or 0, vat=vat or 0, total=total or 0)
    issues = []
    if not items:
        issues.append('No supported line-item rows found')
    if total is None or total <= 0:
        issues.append('Missing or non-positive invoice total')
    if subtotal is None or vat is None:
        issues.append('Missing explicit subtotal or tax')
    if invoice.invoice_number == 'UNKNOWN' or not invoice.invoice_date:
        issues.append('Missing invoice number or date')
    if currency == 'UNKNOWN':
        issues.append('Currency could not be determined')
    if subtotal is not None and abs(sum(i.line_total for i in items) - subtotal) > 0.02:
        issues.append('Parsed line totals do not equal subtotal')
    if subtotal is not None and vat is not None and total is not None and abs(subtotal + vat - total) > 0.02:
        issues.append('Subtotal plus tax does not equal total')
    if any(abs(i.quantity * i.unit_price - i.line_total) > 0.02 for i in items):
        issues.append('Line quantity times price does not equal line total')
    return invoice, issues
