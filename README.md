# AI Finance Controller

**Evidence-driven financial exception investigation and human decision support system.**

## 📌 Overview

AI Finance Controller is an AI-assisted financial control system designed to identify invoice-related exceptions, investigate their root causes, connect findings to supporting evidence, assess financial risk, and recommend appropriate actions for finance teams.

Unlike systems that only flag suspicious transactions, this project focuses on **understanding why an exception occurred and supporting the finance controller's decision with evidence and risk analysis**.

The system keeps the final financial decision with an authorized human decision-maker while maintaining an auditable history of the investigation and decision.

---

## 🎯 Problem Statement

Financial teams often need to verify invoices against multiple sources such as:

- Purchase orders
- Goods receipts
- Approval records
- Financial policies
- Vendor information
- Previously processed invoices

Checking these sources manually can make exception investigation time-consuming and difficult to audit.

The goal of this project is to provide a centralized system that can:

1. Detect financial control exceptions.
2. Investigate the reasons behind those exceptions.
3. Perform root-cause analysis.
4. Build an evidence chain for each finding.
5. Calculate financial risk.
6. Recommend an appropriate action.
7. Allow authorized finance personnel to make the final decision.
8. Maintain an auditable history of the complete process.

---

## 💡 What Makes This Project Different?

Traditional invoice-processing systems generally focus on **transaction processing, validation, or anomaly detection**.

AI Finance Controller focuses on **investigation, explainability, evidence, risk analysis, and human decision support**.

### Key Differences

| Existing Approach | AI Finance Controller |
|---|---|
| Detects an anomaly or exception | Detects the exception and investigates its root cause |
| Provides an alert | Connects findings to supporting evidence and risk factors |
| May automatically trigger an action | Recommends an action while keeping final authorization with a human |
| Limited investigation context | Maintains investigation and audit history |

### Core Idea

**Detect → Investigate → Explain → Evidence → Assess Risk → Recommend → Human Decision → Audit**

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
      ├── AI Analysis
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
Authorized Finance User
      │
      ├── Approve
      ├── Reject
      ├── Hold
      └── Block
      │
      ▼
Audit Trail
```

---

## 🔍 Exception Detection

The system analyzes financial data and identifies different types of control exceptions.

Current detection capabilities include:

- Invoice amount mismatch
- Invoice quantity mismatch
- Duplicate invoice detection
- Missing approval detection
- Policy violation detection
- Vendor anomaly detection
- Data validation failures

Each detected exception is recorded with relevant information so that it can be investigated further.

---

## 🕵️ Investigation & Root Cause Analysis

Detection is only the first step.

The investigation layer attempts to understand **why the exception occurred** by combining:

- Invoice information
- Purchase order information
- Receipt information
- Approval information
- Vendor information
- Policy information
- Exception history
- Contextual financial data
- AI-assisted analysis

The system produces a structured investigation result containing the identified root cause and supporting context.

This allows finance teams to move from:

> "An exception was detected."

to:

> "The system investigated the exception and identified the likely reason behind it."

---

## 🔗 Evidence Chain

The system creates an evidence chain connecting an exception to the information that supports the investigation.

Evidence can include:

- Invoice records
- Purchase orders
- Receipts
- Approval records
- Policy rules
- Vendor information
- Detection results
- Investigation findings
- Risk factors
- Recommendations

The evidence layer improves explainability by allowing finance users to understand **how the system reached its recommendation**.

---

## ⚠️ Risk Analysis

The risk engine evaluates the financial impact and severity of identified exceptions.

Risk assessment considers factors such as:

- Exception severity
- Financial amount
- Number of exceptions
- Missing approvals
- Policy violations
- Duplicate invoice indicators
- Vendor-related anomalies
- Investigation findings

The system produces a risk score and corresponding risk level such as:

- Low
- Medium
- High
- Critical

The risk assessment is then used by the recommendation engine.

---

## 🤖 Recommendation Engine

Based on the detected exceptions, investigation findings, evidence, and risk assessment, the system recommends an appropriate action.

Possible recommendations include:

- **Approve**
- **Hold**
- **Reject**
- **Block Payment**
- **Escalate**

The recommendation is intended to support the finance team rather than replace the final human decision.

---

## 👤 Human-in-the-Loop Decision

The system follows a human-in-the-loop approach.

AI and rule-based components can:

- Detect exceptions
- Investigate issues
- Analyze evidence
- Assess risk
- Recommend actions

However, the final financial decision remains with an authorized finance user.

Authorized users can review the investigation and recommendation before making the final decision.

This reduces the risk of blindly relying on automated financial decisions.

---

## 🔐 Role-Based Access Control

The application includes role-based access control to separate responsibilities.

Current roles include:

| Role | Access |
|---|---|
| Admin | Full system access and user management |
| Finance Controller | Financial review and final decision authority |
| Finance Reviewer | View and review financial information |
| Auditor | Audit and investigation review |

Sensitive operations such as uploading financial data, processing data, and submitting final decisions are restricted based on user permissions.

This provides stronger separation of responsibilities within the financial workflow.

---

## 📄 Document & OCR Ingestion

The system supports financial document ingestion in multiple formats.

Supported formats include:

- CSV
- XLSX
- PDF
- PNG
- JPG / JPEG
- TIFF
- BMP

For scanned financial documents, the OCR pipeline extracts relevant information such as:

- Invoice number
- Vendor
- Purchase order number
- Invoice date
- Amount
- Quantity
- Currency
- Status

The OCR pipeline also provides:

- Field-level confidence scores
- Average extraction confidence
- Low-confidence field identification
- Extraction completeness status
- Manual-review indicators
- Extracted text
- Validated invoice information

This allows document-based financial information to enter the same investigation workflow as structured data.

---

## 📊 Excel Reporting

The project includes an Excel reporting layer for human-readable financial analysis and export.

Generated reports can contain:

### Invoice Analysis

Includes information such as:

- Invoice details
- Exception information
- Risk score
- Risk level
- AI recommendation
- Processing information

### Human Decisions

Includes:

- Invoice ID
- AI recommendation
- Human decision
- Decision comparison
- Decision metadata

### Audit Trail

Includes records of important financial processing and decision activities.

SQLite remains the application's primary persistence layer, while Excel acts as a reporting and export format for finance users.

Generated reports are stored under:

```text
data/reports/
```

---

## 🖥️ Streamlit Interface

The project provides a Streamlit-based frontend for finance users.

### Dashboard

Provides an overview of:

- Processed invoices
- Financial amounts
- Exception counts
- Risk levels
- Recommended actions

### Exceptions

Displays detected financial exceptions and their severity.

### Investigation

Provides investigation details including:

- Invoice information
- Exceptions
- Root causes
- Risk analysis
- Evidence
- Recommendation

### Decisions

Allows authorized users to review AI recommendations and submit final financial decisions according to their role permissions.

### Audit Trail

Provides a historical view of:

- Financial processing
- Investigation results
- Recommendations
- Human decisions
- Audit events

---

## 🏗️ Project Structure

```text
AI-Finance-Controller/
│
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   ├── decision_routes.py
│   │   ├── exception_routes.py
│   │   ├── investigation_routes.py
│   │   ├── ingestion_routes.py
│   │   ├── dynamic_processing_routes.py
│   │   └── document_ingestion_routes.py
│   │
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── jwt_handler.py
│   │   ├── routes.py
│   │   ├── security.py
│   │   └── user_routes.py
│   │
│   ├── audit/
│   │   ├── audit_logger.py
│   │   └── audit_service.py
│   │
│   ├── data/
│   │   ├── loader.py
│   │   └── validator.py
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
│   │   ├── amount_detector.py
│   │   ├── duplicate_invoice.py
│   │   ├── missing_approval.py
│   │   ├── policy_detector.py
│   │   ├── quantity_detector.py
│   │   └── vendor_anomaly.py
│   │
│   ├── evidence/
│   │   ├── evidence_builder.py
│   │   ├── evidence_chain.py
│   │   └── evidence_validator.py
│   │
│   ├── ingestion/
│   │   ├── csv_ingestor.py
│   │   ├── excel_ingestor.py
│   │   ├── entity_loader.py
│   │   ├── ocr_extractor.py
│   │   ├── pdf_extractor.py
│   │   ├── document_ingestor.py
│   │   └── invoice_document_parser.py
│   │
│   ├── investigation/
│   │   ├── ai_analyzer.py
│   │   ├── context_builder.py
│   │   ├── investigator.py
│   │   └── root_cause.py
│   │
│   ├── recommendation/
│   │   ├── action_rules.py
│   │   └── recommendation_engine.py
│   │
│   ├── reporting/
│   │   └── excel_report.py
│   │
│   ├── risk/
│   │   ├── risk_engine.py
│   │   └── risk_factors.py
│   │
│   ├── services/
│   │   ├── finance_controller.py
│   │   └── dynamic_processor.py
│   │
│   ├── models/
│   │   └── financial_models.py
│   │
│   └── main.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── reports/
│   └── ingestion_test/
│
├── frontend/
│   ├── components/
│   │   ├── evidence_panel.py
│   │   ├── exception_card.py
│   │   ├── recommendation_panel.py
│   │   └── risk_indicator.py
│   │
│   ├── pages/
│   │   ├── dashboard.py
│   │   ├── exceptions.py
│   │   ├── investigation.py
│   │   ├── decisions.py
│   │   └── audit_trail.py
│   │
│   └── app.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE
```

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLite
- JWT authentication

### AI & Analysis

- AI-assisted investigation
- Rule-based exception detection
- Root-cause analysis
- Risk scoring
- Evidence-based recommendations

### Document Processing

- PDF processing
- OCR
- Image processing
- CSV ingestion
- Excel ingestion

### Frontend

- Streamlit

### Reporting

- OpenPyXL
- Excel reporting

### Testing

- Pytest

### Development Environment

- GitHub
- GitHub Codespaces
- Visual Studio Code

---

## 🔌 API Endpoints

The backend provides APIs for major financial control operations.

Examples include:

```text
Authentication
    ├── Login
    └── User management

Financial Processing
    ├── Invoice ingestion
    ├── Dynamic processing
    └── Document ingestion

Exception Management
    ├── Exception retrieval
    └── Exception analysis

Investigation
    ├── Investigation results
    └── Root-cause analysis

Decision Management
    ├── Decision submission
    └── Decision history

Audit
    └── Audit trail
```

The FastAPI application exposes interactive API documentation when the backend is running.

---

## 🧪 Testing

The project includes automated tests covering major components of the financial control workflow.

Current test suite:

```text
24 passed
```

Run the tests using:

```bash
python -m pytest -v
```

or:

```bash
python -m pytest -q
```

The test suite validates functionality across:

- Data validation
- Exception detection
- Investigation
- Evidence generation
- Risk analysis
- Recommendations
- Decisions
- Authentication
- Document ingestion
- OCR processing
- Reporting
- API behavior

---

## 🚀 Running the Project in GitHub Codespaces

### 1. Clone the Repository

```bash
git clone https://github.com/lekha-sri-nag/AI-Finance-Controller.git
cd AI-Finance-Controller
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Tests

```bash
python -m pytest -v
```

### 6. Start the FastAPI Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The backend will be available through the Codespaces forwarded port.

### 7. Start the Streamlit Frontend

Open a second terminal and activate the virtual environment:

```bash
source .venv/bin/activate
```

Then run:

```bash
streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501
```

Open the forwarded Streamlit port to access the application.

---

## 📌 Example Scenario

Consider an invoice:

```text
Invoice ID: INV-TEST-001
Invoice Amount: ₹25,000
Risk Score: 90
Risk Level: Critical
Exceptions: 3
Recommended Action: Block Payment
```

The system does not stop at detecting the exceptions.

It:

1. Identifies the financial exceptions.
2. Investigates the invoice context.
3. Determines likely root causes.
4. Builds an evidence chain.
5. Calculates the financial risk.
6. Generates a recommendation.
7. Presents the recommendation to an authorized finance user.
8. Records the final human decision.
9. Maintains the complete audit history.

This demonstrates the project's core principle:

**The system supports the financial controller's decision rather than blindly making the decision.**

---

## 🔐 Security & Governance

The system incorporates several controls intended for financial workflows:

- JWT-based authentication
- Role-based authorization
- Restricted financial operations
- Human approval for final decisions
- Evidence-backed recommendations
- Audit trail
- Decision history
- Separation of reviewer and decision-maker responsibilities

The architecture is designed around the principle that automated analysis should remain **explainable, reviewable, and auditable**.

---

## 📈 Current Project Status

### Implemented

- [x] Financial data ingestion
- [x] Data validation
- [x] Invoice exception detection
- [x] Amount mismatch detection
- [x] Quantity mismatch detection
- [x] Duplicate invoice detection
- [x] Missing approval detection
- [x] Policy violation detection
- [x] Vendor anomaly detection
- [x] Investigation engine
- [x] Root-cause analysis
- [x] AI-assisted analysis
- [x] Evidence chain generation
- [x] Risk scoring
- [x] Risk classification
- [x] Action recommendation
- [x] Human-in-the-loop decisions
- [x] Decision validation
- [x] Decision history
- [x] JWT authentication
- [x] Role-based access control
- [x] CSV ingestion
- [x] Excel ingestion
- [x] PDF document ingestion
- [x] OCR-based invoice extraction
- [x] OCR confidence analysis
- [x] Manual-review indicators
- [x] SQLite persistence
- [x] Audit trail
- [x] Streamlit dashboard
- [x] Exception interface
- [x] Investigation interface
- [x] Decision interface
- [x] Audit interface
- [x] Excel financial reporting
- [x] Automated testing

---

## 🔮 Future Enhancements

Possible future improvements include:

- Integration with enterprise ERP systems
- Advanced machine-learning-based anomaly detection
- More sophisticated vendor risk modeling
- Additional financial document formats
- Advanced analytics dashboards
- Multi-organization deployment
- Cloud-native production deployment
- Integration with enterprise identity providers
- Enhanced explainability and model monitoring

---

## 📂 Data & Privacy

The project uses sample and test financial data for development and demonstration purposes.

Sensitive production financial information should not be committed to the repository.

The project excludes generated reports, local databases, environment files, uploaded documents, and other runtime artifacts where appropriate through `.gitignore`.


---

## 👩‍💻 Author

**Vutukuri Lekha Sri Nag**

AI Finance Controller — Evidence-driven financial exception investigation and human decision support system.

GitHub:

https://github.com/lekha-sri-nag/AI-Finance-Controller