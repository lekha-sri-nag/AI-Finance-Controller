# AI Finance Controller

**Evidence-driven financial exception investigation and human decision support system.**

## Live Demo

**Application:**
https://ai-finance-controller-1-rqid.onrender.com

**GitHub Repository:**
https://github.com/lekha-sri-nag/AI-Finance-Controller

---

## Overview

AI Finance Controller is an AI-assisted financial control system designed to identify invoice-related exceptions, investigate their root causes, connect findings to supporting evidence, assess financial risk, and recommend appropriate actions for finance teams.

Unlike systems that only flag suspicious transactions, this project focuses on **understanding why an exception occurred and supporting the finance controller's decision with evidence and risk analysis**.

The system keeps the final financial decision with an authorized human decision-maker while maintaining an auditable history of the investigation and decision.

---

## Problem Statement

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
3. Perform root-cause analysis.
4. Build an evidence chain for each finding.
5. Calculate financial risk.
6. Recommend an appropriate action.
7. Allow authorized finance personnel to make the final decision.
8. Maintain an auditable history of the complete process.

---

## What Makes This Project Different?

Traditional invoice-processing systems generally focus on **transaction processing, validation, or anomaly detection**.

AI Finance Controller focuses on **investigation, explainability, evidence, risk analysis, and human decision support**.

| Existing Approach                   | AI Finance Controller                                               |
| ----------------------------------- | ------------------------------------------------------------------- |
| Detects an anomaly or exception     | Detects the exception and investigates its root cause               |
| Provides an alert                   | Connects findings to supporting evidence and risk factors           |
| May automatically trigger an action | Recommends an action while keeping final authorization with a human |
| Limited investigation context       | Maintains investigation and audit history                           |

### Core Idea

**Detect -> Investigate -> Explain -> Evidence -> Assess Risk -> Recommend -> Human Decision -> Audit**

---

## System Workflow

```text
Financial Data
      |
      v
Data Validation
      |
      v
Exception Detection
      |
      v
Exception Found
      |
      v
Investigation
      |
      +-- Root Cause Analysis
      +-- Context Analysis
      +-- AI-Assisted Analysis
      +-- Evidence Collection
      |
      v
Evidence Chain
      |
      v
Risk Analysis
      |
      v
Action Recommendation
      |
      v
Authorized Finance User
      |
      +-- Approve
      +-- Reject
      +-- Hold
      +-- Block
      |
      v
Audit Trail
```

---

## Exception Detection

The system analyzes financial data and identifies different types of control exceptions.

Current detection capabilities include:

* Invoice amount mismatch
* Invoice quantity mismatch
* Duplicate invoice detection
* Missing approval detection
* Policy violation detection
* Vendor anomaly detection
* Data validation failures

Each detected exception is recorded with relevant information so that it can be investigated further.

---

## Investigation and Root Cause Analysis

Detection is only the first step.

The investigation layer attempts to understand **why the exception occurred** by combining:

* Invoice information
* Purchase order information
* Receipt information
* Approval information
* Vendor information
* Policy information
* Exception history
* Contextual financial data
* AI-assisted analysis

The system produces a structured investigation result containing the identified root cause and supporting context.

This allows finance teams to move from:

> "An exception was detected."

to:

> "The system investigated the exception and identified the likely reason behind it."

---

## Evidence Chain

The system creates an evidence chain connecting an exception to the information that supports the investigation.

Evidence can include:

* Invoice records
* Purchase orders
* Receipts
* Approval records
* Policy rules
* Vendor information
* Detection results
* Investigation findings
* Risk factors
* Recommendations

The evidence layer improves explainability by allowing finance users to understand **how the system reached its recommendation**.

---

## Risk Analysis

The risk engine evaluates the financial impact and severity of identified exceptions.

Risk assessment considers factors such as:

* Exception severity
* Financial amount
* Number of exceptions
* Missing approvals
* Policy violations
* Duplicate invoice indicators
* Vendor-related anomalies
* Investigation findings

The system produces a risk score and corresponding risk level such as:

* Low
* Medium
* High
* Critical

The risk assessment is then used by the recommendation engine.

---

## Recommendation Engine

Based on the detected exceptions, investigation findings, evidence, and risk assessment, the system recommends an appropriate action.

Possible recommendations include:

* **Approve**
* **Hold**
* **Reject**
* **Block Payment**
* **Escalate**

The recommendation is intended to support the finance team rather than replace the final human decision.

---

## Human-in-the-Loop Decision

The system follows a human-in-the-loop approach.

AI and rule-based components can:

* Detect exceptions
* Investigate issues
* Analyze evidence
* Assess risk
* Recommend actions

However, the final financial decision remains with an authorized finance user.

Authorized users can review the investigation and recommendation before making the final decision.

This reduces the risk of blindly relying on automated financial decisions.

---

## Streamlit Interface

The project provides a Streamlit-based frontend for finance users.

### Dashboard

Provides an overview of:

* Processed invoices
* Financial amounts
* Exception counts
* Risk levels
* Recommended actions
* Financial analysis report

### Exceptions

Displays detected financial exceptions and their severity.

### Investigation

Provides investigation details including:

* Invoice information
* Exceptions
* Root causes
* Risk analysis
* Evidence
* Recommendation

### Decisions

Allows authorized users to review AI recommendations and submit final financial decisions according to their role permissions.

### Audit Trail

Provides a historical view of:

* Financial processing
* Investigation results
* Recommendations
* Human decisions
* Audit events

---

## Supported File Uploads

The application supports the following invoice/document formats:

* CSV
* XLSX
* PDF
* PNG
* JPG
* JPEG

Document processing includes structured data ingestion and OCR-based extraction where applicable.

---

## Project Structure

```text
AI-Finance-Controller/
|
+-- app/
|   +-- api/
|   +-- auth/
|   +-- audit/
|   +-- data/
|   +-- database/
|   +-- decision/
|   +-- detection/
|   +-- evidence/
|   +-- ingestion/
|   +-- investigation/
|   +-- recommendation/
|   +-- reporting/
|   +-- risk/
|   +-- services/
|   +-- models/
|   +-- main.py
|
+-- data/
|   +-- raw/
|   +-- processed/
|   +-- reports/
|   +-- ingestion_test/
|
+-- frontend/
|   +-- components/
|   +-- pages/
|   +-- app.py
|
+-- tests/
|
+-- .env.example
+-- .gitignore
+-- README.md
+-- requirements.txt
+-- LICENSE
```

---

## Technology Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLite
* JWT authentication

### AI and Analysis

* AI-assisted investigation
* Rule-based exception detection
* Root-cause analysis
* Risk scoring
* Evidence-based recommendations

### Document Processing

* PDF processing
* OCR
* Image processing
* CSV ingestion
* Excel ingestion

### Frontend

* Streamlit

### Reporting

* OpenPyXL
* Excel reporting

### Testing

* Pytest

### Deployment

* Render
* Docker

### Development

* GitHub
* Visual Studio Code

---

## API Capabilities

The backend provides APIs for major financial control operations.

```text
Authentication
    +-- Login
    +-- Role-based access

Financial Processing
    +-- Invoice ingestion
    +-- Dynamic processing
    +-- Document ingestion

Exception Management
    +-- Exception detection
    +-- Exception retrieval

Investigation
    +-- Investigation results
    +-- Root-cause analysis
    +-- Evidence chain

Risk and Recommendation
    +-- Risk analysis
    +-- Action recommendation

Decision Management
    +-- Human decision submission
    +-- Decision history

Audit
    +-- Audit trail
```

The FastAPI application also provides interactive API documentation when the backend is running.

---

## Testing

The project includes automated tests covering the major financial control workflow.

Current test result:

```text
24 passed
```

Run the test suite using:

```bash
python -m pytest
```

The tests cover:

* Data validation
* Exception detection
* Investigation
* Evidence generation
* Risk analysis
* Recommendations
* Decisions
* Controller processing

The application has also been verified through live API requests and the deployed Streamlit frontend.

---

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/lekha-sri-nag/AI-Finance-Controller.git
cd AI-Finance-Controller
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the FastAPI backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 6. Start the Streamlit frontend

Open another terminal and run:

```bash
streamlit run frontend/app.py --server.port 8501
```

### 7. Run tests

```bash
python -m pytest
```

---

## Example Scenario

Consider an invoice:

```text
Invoice ID: INV-TEST-001
Invoice Amount: INR 25,000
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

## Project Status

| Component                 | Status    |
| ------------------------- | --------- |
| Invoice ingestion         | Complete  |
| CSV processing            | Tested    |
| Excel processing          | Tested    |
| PDF processing            | Tested    |
| Image processing          | Tested    |
| OCR processing            | Tested    |
| Exception detection       | Complete  |
| Investigation             | Complete  |
| Evidence chain            | Complete  |
| Risk analysis             | Complete  |
| Recommendation engine     | Complete  |
| Human decision workflow   | Complete  |
| Audit trail               | Complete  |
| Role-based authentication | Complete  |
| Excel financial report    | Complete  |
| Automated tests           | 24 passed |
| Production deployment     | Live      |

---

## Author

**Vutukuri Lekha Sri Nag**

AI Finance Controller - Evidence-driven financial exception investigation and human decision support system.

GitHub:
https://github.com/lekha-sri-nag/AI-Finance-Controller
