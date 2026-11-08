# Invoice Reconciliation Agent

A Python command-line demonstration of a four-stage LangGraph workflow:

```text
Document -> Matching -> Discrepancy -> Resolution
```

The current implementation uses predefined invoice records keyed by the five bundled PDF filenames. It demonstrates reconciliation control flow; it does not yet extract invoice values from arbitrary PDF contents.

## Run locally

Validated with Python 3.10.11 on Windows. From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m app.main
```

For macOS/Linux, use `.venv/bin/python` in place of `.\.venv\Scripts\python.exe`.

This is a batch CLI, with no web server or browser interface. It exits after printing JSON results for all five bundled invoices. The active demo pipeline requires no API key or external service.

## Local validation results

Validation date: November 9, 2026. Source revision: `5f3f622a684fe177a52ee109a5448b64ea7aa78f`.

The full console output is recorded in [results/local-run.txt](results/local-run.txt), and [results/requirements-local.txt](results/requirements-local.txt) records the installed dependency versions.

| Sample | Matched PO | Recommendation | Discrepancies |
| --- | --- | --- | --- |
| Invoice_1_Baseline.pdf | PO-2024-001 | auto_approve | None |
| Invoice_2_Scanned.pdf | None | flag_for_review | no_matching_po |
| Invoice_3_Different_Format.pdf | PO-2024-003 | auto_approve | None |
| Invoice_4_Price_Trap.pdf | PO-2024-004 | auto_approve | None |
| Invoice_5_Missing_PO.pdf | PO-2024-005 | auto_approve | None |

These are observed demo decisions, not evidence that the financial decisions are correct or that PDF extraction works.

## Behavior and limitations

- `utils/pdf.py` returns a fixed placeholder string. `agents/document_agent.py` ignores that text and selects hardcoded line items and totals by filename. Unknown filenames are unsupported.
- The scanned sample has no line items and a zero total. It is flagged because no PO matches; OCR is not invoked by the active workflow.
- PO matching uses equal totals first, then case-insensitive description substring overlap. The active matcher does not validate supplier, currency, or explicit PO references, and does not use the fuzzy helper.
- The price-trap sample matches by line items. Its total of GBP 13,476 differs from the PO total of GBP 13,176 by about 2.28%, below the discrepancy agent's 5% threshold. The demo consequently approves it despite the hardcoded ibuprofen unit price differing from the PO.
- The missing-reference sample is approved because its total equals PO-2024-005. A missing reference alone is not flagged.
- Extraction confidence is always set to 0.95, including for the empty scanned sample. Resolution checks only whether discrepancies exist; it does not enforce confidence thresholds.
- `utils/llm.py` is a stub returning an empty list. No LLM extraction was exercised.
- The separate OCR helper expects Poppler and Tesseract, with a hardcoded Windows Tesseract path. OCR was not validated in this run.

Before real invoice processing, implement actual extraction, line-item price/quantity checks, supplier/currency validation, confidence-based review, and regression tests with independently verified expected decisions.

## Project layout

- `app/main.py`: batch CLI and JSON serialization.
- `app/graph.py`: four-stage LangGraph workflow.
- `agents/`: document, matching, discrepancy, and resolution stages.
- `utils/`: schemas, PO loaders, and extraction/matching helpers.
- `data/invoices/`: five bundled sample PDFs.
- `data/purchase_orders.json`: purchase orders used by the active matcher.
- `results/`: captured local output and installed dependency versions.

## Provenance and contributions

Original project: [RitvikSharmaa/invoice-reconciliation-agent](https://github.com/RitvikSharmaa/invoice-reconciliation-agent), by Ritvik Sharma (GitHub: [RitvikSharmaa](https://github.com/RitvikSharmaa)). The imported history contains six original commits, recorded under Ritvik Sharma and RitvikSharmaa.

Local validation and documentation contribution: Ajith Reddy, using the existing local Git author configuration, with Codex assistance. This contribution records the local run, dependency versions, and implementation limitations. At the repository owner's request, this branch records all commit author and committer identities as Ajith Reddy. This is an attribution rewrite, not a claim that Ajith wrote the upstream implementation. The original commit identities remain available locally on `backup/original-authorship`.

Inspect contribution history with:

```bash
git log --format="%h %an <%ae> %s"
git shortlog -sne HEAD
```

## License status

The upstream README claimed MIT licensing, but the checked-out source revision contains no LICENSE file. Obtain clarification from the original author before redistributing under an assumed MIT grant.
