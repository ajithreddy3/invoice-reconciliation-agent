# 🧾 Invoice Reconciliation Agent

An end-to-end **autonomous invoice reconciliation system** that extracts, validates, matches, and reconciles supplier invoices against purchase orders using deterministic rules with intelligent fallbacks.

This project simulates a **real-world finance automation pipeline** used in enterprise procurement, accounting, and ERP systems.

---

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
