# AI Finance Controller

**Evidence-driven financial exception investigation and human decision support system.**

## 📌 Overview

AI Finance Controller is an AI-assisted financial control system designed to identify invoice-related exceptions, investigate their root causes, connect each exception to supporting evidence, assess financial risk, and recommend appropriate actions for finance teams.

Unlike systems that only flag suspicious transactions, this project focuses on **explaining why an exception occurred and supporting the finance controller's decision with evidence and risk analysis**.

The system keeps the final financial decision with a human reviewer while maintaining an audit trail of the investigation and decision.

---

## 🎯 Problem Statement

Financial teams often need to verify invoices against multiple sources such as:

* Purchase orders
* Goods receipts
* Approval records
* Financial policies
* Vendor information
* Previously processed invoices

Checking these sources manually can make exception investigation time-consuming and difficult to audit.

The goal of this project is to provide a centralized system that can:

1. Detect financial control exceptions.
2. Investigate the reasons behind those exceptions.
3. Build an evidence chain for each finding.
4. Calculate the financial risk.
5. Recommend an appropriate action.
6. Allow a finance reviewer to make the final decision.
7. Maintain an auditable history of the complete process.

---

## 💡 What Makes This Project Different?

Traditional invoice-processing systems generally focus on **processing transactions or detecting anomalies**.

AI Finance Controller focuses on **investigation and decision support**.

### Key differences

| Existing Approach               | AI Finance Controller                                                       |
| ------------------------------- | --------------------------------------------------------------------------- |
| Detects an anomaly or exception | Detects the exception and investigates its root cause                       |
| Provides an alert               | Connects findings to supporting evidence and risk factors                   |
| Automated action may be taken   | Recommends an action while keeping the final decision with a human reviewer |

### Core idea

**Detect → Investigate → Explain → Assess Risk → Recommend → Human Decision → Audit**

---

## 🔄 System Workflow

```text
Financial Data
      │
      ▼
Data Validation
      │
      ▼
Exception Detection
      │
      ▼
Exception Found
      │
      ▼
Investigation
      │
      ├── Root Cause Analysis
      ├── Context Analysis
      └── Evidence Collection
      │
      ▼
Evidence Chain
      │
      ▼
Risk Analysis
      │
      ▼
Action Recommendation
      │
      ▼
Finance Controller
      │
      ├── Approve
      ├── Hold
      ├── Reject
      └── Block
      │
      ▼
Audit Trail
```

---

## 🚨 Exception Detection

The system currently supports detection of multiple financial control exceptions:

* **Amount Mismatch**
* **Quantity Mismatch**
* **Missing Approval**
* **Policy Violation**
* **Vendor Anomaly**
* **Duplicate Invoice**

Each exception contains information such as:

* Exception ID
* Invoice ID
* Exception type
* Severity
* Description
* Detection timestamp
* Status

---

## 🔍 Investigation & Root Cause Analysis

After detecting exceptions, the system investigates the underlying causes.

For example:

**Exception: Amount Mismatch**

```text
Invoice Amount = ₹75,000
Purchase Order = ₹50,000
```

The investigation identifies the root cause:

> Invoice amount does not match the approved purchase order.

The system can similarly investigate quantity, approval, policy, and vendor-related issues.

---

## 📑 Evidence Chain

Every identified exception can be connected to supporting evidence.

Example:

```text
Exception
   │
   ▼
Evidence
   │
   ├── Source Type
   ├── Source Reference
   ├── Description
   └── Confidence
```

Example:

```text
Exception:
Amount Mismatch

Evidence:
Source Type       → Purchase Order
Source Reference  → PO-013
Confidence        → 1.0
```

This makes the investigation explainable and easier to audit.

---

## ⚠️ Risk Analysis

The risk engine evaluates detected exceptions and produces:

* Risk score
* Risk level
* Risk factors
* Risk explanation

Supported risk levels:

```text
Low
Medium
High
Critical
```

For example, the test invoice `INV-013` produced:

```text
Risk Score: 100
Risk Level: Critical
Exceptions: 5
```

---

## 🤖 Recommendation Engine

Based on the calculated risk level, the system generates an action recommendation.

| Risk Level | Recommended Action | Human Review |
| ---------- | ------------------ | ------------ |
| Low        | Approve Payment    | No           |
| Medium     | Review Invoice     | Yes          |
| High       | Hold Payment       | Yes          |
| Critical   | Block Payment      | Yes          |

The recommendation is **not treated as the final financial decision**.

---

## 👤 Human-in-the-Loop Decision

The finance controller retains control over the final decision.

Supported decisions include:

* Approve
* Reject
* Hold
* Block

Each decision records:

* Decision ID
* Invoice ID
* Recommendation ID
* Final decision
* Reviewer
* Timestamp
* Comments

This creates a clear separation between **AI recommendation** and **human authorization**.

---

## 🧾 Audit Trail

The system maintains an audit trail covering:

* Detected exceptions
* Investigation results
* Root causes
* Supporting evidence
* Risk assessment
* AI recommendation
* Human decision
* Reviewer information
* Decision timestamp

This allows the finance team to understand the complete history of an invoice.

---

## 🧪 Example Scenario

The system was tested using invoice `INV-013`.

### Invoice

```text
Invoice ID     : INV-013
Vendor        : XYZ Traders
Amount        : ₹75,000
Quantity      : 100
Status        : Pending
```

### Purchase Order

```text
PO Amount      : ₹50,000
Status         : Approved
```

### Goods Receipt

```text
Received Qty   : 80
```

### Vendor

```text
Vendor         : XYZ Traders
Risk Level     : High
```

### Detected Exceptions

```text
1. Amount Mismatch
2. Missing Approval
3. Quantity Mismatch
4. Policy Violation
5. Vendor Anomaly
```

### Result

```text
Risk Score            : 100
Risk Level            : Critical
Recommendation        : Block Payment
Human Review Required : Yes
Investigation Status  : Completed
```

### Human Decision

```text
Decision               : Block
Reviewer               : finance_reviewer
```

The complete result is then available through the audit trail.

---

## 🏗️ Project Structure

```text
AI-Finance-Controller/
│
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   ├── exception_routes.py
│   │   ├── investigation_routes.py
│   │   └── decision_routes.py
│   │
│   ├── audit/
│   │   ├── audit_logger.py
│   │   └── audit_service.py
│   │
│   ├── controller.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── repositories.py
│   │
│   ├── decision/
│   │   ├── human_decision.py
│   │   └── decision_validator.py
│   │
│   ├── detection/
│   │   ├── amount.py
│   │   ├── quantity.py
│   │   ├── duplicate_invoice.py
│   │   ├── missing_approval.py
│   │   ├── policy.py
│   │   └── vendor_anomaly.py
│   │
│   ├── evidence/
│   │   ├── evidence_builder.py
│   │   ├── evidence_chain.py
│   │   └── evidence_validator.py
│   │
│   ├── investigation/
│   │   ├── investigator.py
│   │   ├── root_cause.py
│   │   ├── context_builder.py
│   │   └── ai_analyzer.py
│   │
│   ├── recommendation/
│   │   ├── recommendation_engine.py
│   │   └── action_rules.py
│   │
│   └── risk/
│       ├── risk_engine.py
│       └── risk_factors.py
│
├── frontend/
│   ├── pages/
│   │   ├── dashboard.py
│   │   ├── exceptions.py
│   │   ├── investigation.py
│   │   ├── decisions.py
│   │   └── audit_trail.py
│   │
│   └── ...
│
├── models/
│   ├── invoice.py
│   ├── purchase_order.py
│   ├── receipt.py
│   ├── approval.py
│   ├── policy.py
│   ├── vendor.py
│   ├── exception.py
│   ├── evidence.py
│   ├── risk_result.py
│   ├── recommendation.py
│   └── decision.py
│
├── tests/
│   ├── test_detection.py
│   ├── test_risk_engine.py
│   ├── test_recommendation.py
│   ├── test_investigation.py
│   ├── test_evidence.py
│   ├── test_decision.py
│   └── test_controller.py
│
├── data/
├── docs/
├── scripts/
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite

### Frontend

* Streamlit

### Testing

* Pytest

### Development Environment

* GitHub Codespaces
* Visual Studio Code

---

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

### Test Invoice API

```http
GET /invoices/test
```

### Process Invoice

```http
POST /invoices/process
```

### Investigation

```http
GET /invoices/{invoice_id}/investigation
```

### Submit Human Decision

```http
POST /decisions/
```

### Get Invoice Decisions

```http
GET /decisions/{invoice_id}
```

---

## 🧪 Testing

The project currently includes automated tests covering:

* Exception detection
* Risk calculation
* Recommendation generation
* Investigation
* Evidence validation
* Human decision creation and validation
* End-to-end controller processing

Current automated test status:

```text
24 tests passed
```

The application has also been verified through live API requests and the Streamlit frontend.

---

## 🚀 Running the Project

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd AI-Finance-Controller
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Start the Streamlit frontend

In another terminal:

```bash
streamlit run frontend/app.py --server.port 8501
```

### 6. Run tests

```bash
python -m pytest -v
```

---

## 📊 Current Project Status

| Component               | Status       |
| ----------------------- | ------------ |
| Invoice validation      | ✅ Complete   |
| Exception detection     | ✅ Complete   |
| Risk engine             | ✅ Complete   |
| Investigation           | ✅ Complete   |
| Root cause analysis     | ✅ Complete   |
| Evidence chain          | ✅ Complete   |
| Recommendation engine   | ✅ Complete   |
| Human decision          | ✅ Complete   |
| Database persistence    | ✅ Complete   |
| Audit trail             | ✅ Complete   |
| FastAPI backend         | ✅ Working    |
| Streamlit frontend      | ✅ Working    |
| Automated tests         | ✅ 24 passing |
| End-to-end verification | ✅ Complete   |

---

## 🔐 Design Principle

The system follows a **human-in-the-loop financial control model**.

AI is used to:

* Detect
* Investigate
* Explain
* Assess
* Recommend

The finance controller remains responsible for the **final financial decision**.

This approach is designed to improve transparency, accountability, and auditability rather than completely replacing human financial control.

---

## 📌 Future Enhancements

Potential future improvements include:

* Real invoice document ingestion
* OCR-based invoice extraction
* Advanced anomaly detection models
* More sophisticated vendor risk scoring
* LLM-powered investigation summaries
* Role-based authentication
* Advanced audit analytics
* Production database support
* Cloud deployment
* Automated notification workflows

---

## 👩‍💻 Project

**AI Finance Controller**

An evidence-driven financial exception investigation and human decision support system.
