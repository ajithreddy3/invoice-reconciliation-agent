# 🧾 Invoice Reconciliation Agent

An end-to-end **autonomous invoice reconciliation system** that extracts, validates, matches, and reconciles supplier invoices against purchase orders using deterministic rules with intelligent fallbacks.

This project simulates a **real-world finance automation pipeline** used in enterprise procurement, accounting, and ERP systems.

---

📄 Written Analysis
Overview

This project implements an agent-based invoice reconciliation system designed to automatically extract, validate, and reconcile supplier invoices against existing purchase orders. The system simulates a realistic enterprise finance workflow, where invoices may arrive in varying formats, contain discrepancies, or lack clear references to purchase orders.

The solution focuses on robustness, explainability, and deterministic decision-making, rather than relying solely on black-box LLM behavior.

System Architecture

The system is built using a multi-agent architecture orchestrated via LangGraph, where each agent is responsible for a clearly defined task:

Document Agent
Extracts structured invoice data from PDF documents using deterministic parsing, with optional OCR and LLM fallback for unstructured layouts.

Matching Agent
Attempts to match the extracted invoice against known purchase orders using:

Exact total matching

Line-item comparison

Fuzzy string similarity for reordered or slightly altered descriptions

Discrepancy Agent
Identifies mismatches such as:

Missing purchase orders

Price variances

Quantity inconsistencies

Total amount deviations

Resolution Agent
Assigns a final recommendation (auto_approve or flag_for_review) based on confidence thresholds and detected discrepancies.

This modular design allows each agent to evolve independently and mirrors how production-grade decision pipelines are typically structured.

Data Handling & Extraction Strategy

Invoice PDFs are processed using deterministic PDF text extraction wherever possible. This ensures predictable behavior and avoids unnecessary dependency on external services.

For cases involving scanned or poorly structured documents, the system supports:

OCR-based extraction (optional)

LLM-assisted fallback for line-item recovery

If all extraction methods fail, the system still produces a valid output with reduced confidence, ensuring graceful degradation rather than system failure.

Purchase Order Matching Logic

Purchase orders are loaded from structured JSON files and indexed in memory for fast access.

Matching is performed using a multi-stage strategy:

Exact total match (highest confidence)

Line-item aggregation match

Fuzzy description similarity (to handle reordered or reformatted items)

Each successful match is assigned a confidence score, which directly influences the final resolution decision.

Discrepancy Detection & Confidence Scoring

The system explicitly tracks discrepancies rather than hiding them. Each discrepancy includes:

Type

Severity

Supporting numerical evidence

A confidence score is computed based on:

Extraction reliability

Matching accuracy

Presence or absence of discrepancies

This makes every automated decision auditable and explainable, a critical requirement in financial systems.

Decision Making & Explainability

Final decisions are derived from confidence thresholds:

High confidence + no discrepancies → auto_approve

Low confidence or unresolved issues → flag_for_review

Each output includes:

A clear recommendation

A structured breakdown of discrepancies (if any)

A human-readable reasoning summary

This ensures that downstream users understand why a decision was made, not just what decision was made.

Design Philosophy

The system prioritizes:

Determinism over blind automation

Transparency over complexity

Graceful failure over brittle pipelines

Rather than forcing LLM usage everywhere, the architecture uses AI only where it adds value, making the system practical, reliable, and production-aligned.

Conclusion

This project demonstrates how agent-based architectures can be applied to real-world financial reconciliation problems. By combining deterministic logic, fuzzy matching, and optional AI assistance, the system achieves a balance between automation and reliability.

The result is a scalable, explainable, and extensible invoice reconciliation pipeline suitable for enterprise environments.

## 🚀 Overview

Invoice reconciliation is a critical but error-prone business process. Invoices often arrive in different formats (PDFs, scans, inconsistent layouts) and must be validated against purchase orders before payment approval.

This system automates that workflow by:

* Extracting structured data from invoices
* Matching invoices to purchase orders
* Detecting discrepancies (price, totals, missing POs)
* Producing clear, explainable reconciliation decisions

The result is a **fully automated, explainable, and extensible reconciliation engine**.

---

## ✨ Key Features

### 📄 Invoice Processing

* Supports **multiple invoice formats**
* Handles clean PDFs and scanned documents
* Line-item level extraction
* Deterministic parsing with intelligent fallback logic

### 🔍 Purchase Order Matching

* Matches invoices to POs using:

  * Total amount comparison
  * Line-item alignment
  * Supplier and currency validation
* Robust handling of missing or ambiguous PO references

### ⚠️ Discrepancy Detection

* Identifies:

  * Missing purchase orders
  * Price mismatches
  * Total mismatches
* Produces structured discrepancy reports with severity levels

### 🤖 Agent-Based Architecture

* Modular agent pipeline
* Each agent has a **single responsibility**
* Easily extensible for OCR, embeddings, or LLM upgrades

### 🧠 Explainable Decisions

* Every reconciliation includes:

  * Confidence scores
  * Explicit reasoning
  * Clear approval / review recommendations

---

## 🏗️ Architecture

```
Invoice PDF
   ↓
Document Agent
   ↓
Matching Agent
   ↓
Discrepancy Agent
   ↓
Resolution Agent
   ↓
Final Reconciliation Decision
```

Each stage is isolated, testable, and independently improvable.

---

## 📁 Project Structure

```
invoice-reconciliation-agent/
│
├── agents/
│   ├── document_agent.py        # Invoice extraction
│   ├── matching_agent.py        # PO matching logic
│   ├── discrepancy_agent.py     # Discrepancy detection
│   └── resolution_agent.py      # Final decision logic
│
├── app/
│   ├── graph.py                 # Agent workflow graph
│   └── main.py                  # Entry point
│
├── utils/
│   ├── pdf.py                   # PDF text extraction
│   ├── ocr.py                   # OCR utilities (optional)
│   ├── llm.py                   # Intelligent fallback logic
│   ├── fuzzy.py                 # Fuzzy matching helpers
│   ├── confidence.py            # Confidence scoring
│   ├── po_loader.py             # Purchase order loading
│   └── schemas.py               # Pydantic data models
│
├── data/
│   ├── invoices/                # Sample invoice PDFs
│   └── purchase_orders.json     # Purchase order dataset
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/RitvikSharmaa/invoice-reconciliation-agent.git
cd invoice-reconciliation-agent
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

```bash
python -m app.main
```

The system will process all invoices in `data/invoices/` and print structured reconciliation results to the console.

---

## 📊 Example Output (Simplified)

```json
{
  "filename": "Invoice_1_Baseline.pdf",
  "matched_po": "PO-2024-001",
  "discrepancies": [],
  "recommended_action": "auto_approve",
  "confidence": 0.95,
  "reasoning": "Invoice matched PO by total and line items"
}
```

Each result includes:

* Extracted invoice data
* Matched purchase order (if any)
* Discrepancy list
* Confidence scores
* Final recommendation

---

## 🧪 Test Coverage (Scenario-Based)

The provided sample invoices intentionally cover:

| Scenario                    | Status          |
| --------------------------- | --------------- |
| Clean invoice + matching PO | ✅ Auto-approved |
| Scanned invoice             | ⚠️ Flagged      |
| Different invoice layout    | ✅ Auto-approved |
| Price discrepancy           | ⚠️ Flagged      |
| Missing PO reference        | ⚠️ Flagged      |

This ensures realistic, production-style behavior.

---

## 🧠 Design Philosophy

* **Deterministic first**: predictable, auditable logic
* **Fallback-driven**: resilience to missing or messy data
* **Explainability over black-box AI**
* **Production-ready structure**, not demo scripts

This system is designed to mirror how **real finance automation platforms** are built.

---

## 🔮 Future Improvements

* OCR integration with Tesseract or cloud vision APIs
* Vector-based line item matching
* Multi-currency reconciliation
* ERP / SAP integration
* Async batch processing
* Web dashboard for review queues

---

## 👤 Author

**Ritvik Sharma**
AI / ML Engineer
GitHub: [https://github.com/RitvikSharmaa](https://github.com/RitvikSharmaa)

---

## 📜 License

This project is open-source and available under the MIT License.
