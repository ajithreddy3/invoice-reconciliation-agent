# Invoice Reconciliation Agent

A Python CLI that reads invoice PDF contents, extracts structured fields and line items, matches purchase orders, checks discrepancies, and recommends approval or manual review through a four-stage LangGraph workflow.

```text
PDF contents -> Document -> Matching -> Discrepancy -> Resolution
```

Extraction is content-based: renaming a PDF does not change its extracted values. The parser supports English invoices with text rows containing description, quantity, unit, unit price, and line total. Other layouts require parser extensions and are flagged when completeness checks fail.

## Run locally

Validated on Windows with Python 3.10.11. From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# Process bundled samples
.\.venv\Scripts\python.exe -m app.main
# Process your own file or a directory of PDFs
.\.venv\Scripts\python.exe -m app.main "C:\invoices\supplier-invoice.pdf"
.\.venv\Scripts\python.exe -m app.main "C:\invoices"
```

On macOS/Linux, use `.venv/bin/python` instead. This is a batch CLI that prints JSON and exits; there is no web server. No API key or LLM service is required.

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

## Provenance and contributions

Original project: [RitvikSharmaa/invoice-reconciliation-agent](https://github.com/RitvikSharmaa/invoice-reconciliation-agent), by Ritvik Sharma ([RitvikSharmaa](https://github.com/RitvikSharmaa)). Imported source revision: `5f3f622a684fe177a52ee109a5448b64ea7aa78f`; the original history contained six commits.

Local contribution: Ajith Reddy, with Codex assistance, implemented content-based extraction, conservative reconciliation checks, CLI file/directory input, regression tests, and result documentation.

At the user's request, the working branch records all commit author and committer identities as Ajith Reddy. This is an attribution rewrite, not a claim that Ajith wrote the upstream implementation. The original identities remain available locally on `backup/original-authorship`.

## License status

The upstream README claimed MIT licensing, but the imported revision contains no LICENSE file. The licensing grant remains unverified.
