# Invoice Reconciliation Agent

**Author: [Ajith Reddy](https://github.com/ajithreddy3)**

Check supplier invoices against purchase orders before payment. This Python application reads invoice PDFs, compares quantities and prices with purchase orders, and explains whether an invoice can be approved or needs manual review.

**Stack:** Python, LangGraph, Pydantic, pdfplumber, PDFium, optional Tesseract OCR.

**Verified locally:** 5 sample invoices processed, 2 recommended approvals, 3 flagged for review, and all 8 regression tests passed. Scanned-document recognition requires a separate Tesseract installation and has not been validated locally.

## Use case

Accounts-payable and procurement teams need to confirm that suppliers billed the agreed amounts. If a purchase order specifies 100 kg at GBP 80/kg but the invoice charges GBP 88/kg, this application flags the price difference rather than recommending approval.

Each result includes extracted invoice data, a matched purchase order when available, discrepancies, and a recommendation. This CLI prototype supports invoice review; it does not execute payments or integrate with an accounting system.

```text
PDF contents -> Document -> Matching -> Discrepancy -> Resolution
```

Invoice values come from the PDF contents, not its filename. The current parser supports English invoice rows containing description, quantity, unit, unit price, and line total. See the extraction limitations below for layouts that require extensions.

## Run locally

Validated on Windows with Python 3.10.11. In PowerShell:

```powershell
git clone https://github.com/ajithreddy3/invoice-reconciliation-agent.git
cd invoice-reconciliation-agent
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# Process bundled samples
.\.venv\Scripts\python.exe -m app.main
# Process your own file or a directory of PDFs
.\.venv\Scripts\python.exe -m app.main "C:\invoices\supplier-invoice.pdf"
.\.venv\Scripts\python.exe -m app.main "C:\invoices"
```

On macOS/Linux, use `.venv/bin/python` instead. This is a batch CLI that prints JSON and exits; there is no web server. No API key or LLM service is required.

## Sample input and observed output

Run the bundled [baseline invoice](data/invoices/Invoice_1_Baseline.pdf) against `data/purchase_orders.json`:

```powershell
.\.venv\Scripts\python.exe -m app.main data/invoices/Invoice_1_Baseline.pdf
```

Confirmed locally on November 9, 2026: the command completed successfully (exit code 0), extracted four line items, and matched `PO-2024-001` with no discrepancies.

| Extracted field | Observed value |
| --- | --- |
| Invoice number | INV-2024-1001 |
| Supplier | PharmaChem Supplies Ltd |
| Invoice date | 15 January 2024 |
| Currency | GBP |
| Subtotal | 7,977.50 |
| VAT | 1,595.50 |
| Total | 9,573.00 |
| Matched PO | PO-2024-001 |
| Recommendation | auto_approve |

Selected fields from the actual JSON output:

```json
{
  "discrepancies": [],
  "extraction_confidence": 0.9,
  "po_match_confidence": 1.0,
  "recommended_action": "auto_approve",
  "agent_reasoning": "Parsed invoice fields and line items from PDF contents | PO matched; validation passed"
}
```

The complete output, including extracted line items and the matched purchase order, is saved in [results/sample-input-run.txt](results/sample-input-run.txt). This confirms the baseline sample; supported-layout limitations still apply to other invoices.

## Extraction and validation

- PDFium repairs PDF structure before pdfplumber extracts page text. This also handles the malformed bundled price-trap PDF.
- Empty text pages are rendered through PDFium and passed to Tesseract. Install Tesseract separately and place it on PATH, or set `TESSERACT_CMD` to its executable. The active pipeline does not require Poppler.
- The parser reads invoice number/date, supplier (first text line), PO reference, currency, subtotal, tax, total, and supported line-item rows. It recognizes item codes before or after descriptions.
- Incomplete fields, unsupported rows, inconsistent arithmetic, invalid PDFs, and OCR failures require review. Missing amounts are represented as zero with explicit discrepancies; they are not eligible for approval.
- Explicit PO references take priority. Without a reference, a unique supplier/currency/total match is a review candidate only.
- Validation compares supplier, currency, total, line quantities, units, prices, and line totals. Approval requires a matched PO, complete extraction, and no discrepancies.

Amounts support comma thousands separators and decimal points. The parser supports explicit GBP/USD/EUR codes and pound/euro/dollar symbols (a bare dollar symbol is interpreted as USD). It is not a universal invoice parser: wrapped descriptions, reordered columns, decimal commas, discounts, complex tax structures, and other languages may need extensions. Extraction confidence is a heuristic, not a calibrated probability. These sample checks do not establish production accuracy.

## Local results

Validation date: November 9, 2026. Full current output: [results/content-extraction-run.txt](results/content-extraction-run.txt).

| Sample | Recommendation | Evidence |
| --- | --- | --- |
| Baseline | auto_approve | Extracted four lines; PO and values match |
| Scanned | flag_for_review | Tesseract unavailable locally; explicit extraction failure |
| Different format | auto_approve | Extracted four lines with trailing item codes; PO matches |
| Price trap | flag_for_review | Unit price, line total, and invoice total differ from PO |
| Missing PO | flag_for_review | Candidate PO found, but invoice has no explicit PO reference |

The earlier hardcoded implementation's output is retained in [results/local-run.txt](results/local-run.txt) as historical evidence, not current behavior. Installed versions are recorded in [results/requirements-local.txt](results/requirements-local.txt).

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

Tests cover bundled text layouts and PDF repair, renamed PDFs, an independently generated PDF, changed PDF contents, arithmetic inconsistency, missing/invalid files, incomplete extraction, and the OCR path. OCR invocation is mocked in tests; actual Tesseract recognition was not validated on this machine.

## Project layout

- `app/`: batch CLI and LangGraph orchestration.
- `agents/`: document extraction, PO matching, discrepancy checks, and resolution.
- `utils/pdf.py`: actual PDF text extraction and optional OCR.
- `utils/invoice_parser.py`: content-based field and row parsing.
- `utils/schemas.py`: structured state and output models.
- `data/invoices/`: bundled PDFs.
- `data/purchase_orders.json`: purchase orders used for matching.
- `tests/`: extraction and workflow regression checks.
- `results/`: current and historical run evidence.

Legacy `utils/ocr.py` and `utils/llm.py` are not used by the active pipeline.

## Author

**Ajith Reddy**

GitHub: [ajithreddy3](https://github.com/ajithreddy3)

Email: [ajithparne@gmail.com](mailto:ajithparne@gmail.com)

Implemented content-based PDF extraction, reconciliation validation, CLI improvements, regression tests, sample execution, and documentation.

## License status

No LICENSE file is included. A redistribution license has not been established.
