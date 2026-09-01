from fastapi import APIRouter, HTTPException

from models.exception import ExceptionRecord
from app.investigation.investigator import investigate_invoice
from app.evidence.evidence_builder import build_evidence
from app.evidence.evidence_chain import build_evidence_chain


router = APIRouter(
    prefix="/invoices",
    tags=["investigation"]
)


@router.get("/{invoice_id}/investigation")
def get_invoice_investigation(invoice_id: str):
    """
    Return detailed investigation results for an invoice.
    """

    # ---------------------------------------------------------
    # 1. Temporary test invoice
    # ---------------------------------------------------------
    if invoice_id != "INV-013":
        raise HTTPException(
            status_code=404,
            detail=f"Invoice {invoice_id} not found"
        )

    invoice = {
        "invoice_id": "INV-013",
        "vendor_id": "V-002",
        "purchase_order_id": "PO-013",
        "invoice_date": "2026-08-27",
        "amount": 75000,
        "quantity": 100,
        "currency": "INR",
        "status": "Pending"
    }

    # ---------------------------------------------------------
    # 2. Purchase Order
    # ---------------------------------------------------------
    purchase_order = {
        "purchase_order_id": "PO-013",
        "vendor_id": "V-002",
        "order_date": "2026-08-20",
        "total_amount": 50000,
        "currency": "INR",
        "status": "Approved"
    }

    # ---------------------------------------------------------
    # 3. Goods Receipt
    # ---------------------------------------------------------
    receipt = {
        "receipt_id": "REC-013",
        "purchase_order_id": "PO-013",
        "receipt_date": "2026-08-27",
        "quantity_received": 80,
        "received_amount": 40000,
        "status": "Received"
    }

    # ---------------------------------------------------------
    # 4. Vendor
    # ---------------------------------------------------------
    vendor = {
        "vendor_id": "V-002",
        "vendor_name": "XYZ Traders",
        "tax_id": "GST67890",
        "category": "Electronics",
        "risk_level": "High",
        "active": True
    }

    # ---------------------------------------------------------
    # 5. Detected Exceptions
    # ---------------------------------------------------------
    exception_data = [
        {
            "exception_id": "EXC-AMOUNT-INV-013",
            "invoice_id": "INV-013",
            "exception_type": "Amount Mismatch",
            "severity": "High",
            "description": (
                "Invoice amount is ₹75,000, "
                "but purchase order amount is ₹50,000."
            ),
            "detected_at": "2026-08-27T10:00:00",
            "status": "Open"
        },
        {
            "exception_id": "EXC-APPROVAL-INV-013",
            "invoice_id": "INV-013",
            "exception_type": "Missing Approval",
            "severity": "High",
            "description": (
                "Invoice INV-013 has no approval record."
            ),
            "detected_at": "2026-08-27T10:01:00",
            "status": "Open"
        },
        {
            "exception_id": "EXC-QUANTITY-INV-013",
            "invoice_id": "INV-013",
            "exception_type": "Quantity Mismatch",
            "severity": "High",
            "description": (
                "Invoice quantity is 100, "
                "but received quantity is 80."
            ),
            "detected_at": "2026-08-27T10:02:00",
            "status": "Open"
        },
        {
            "exception_id": "EXC-POLICY-INV-013",
            "invoice_id": "INV-013",
            "exception_type": "Policy Violation",
            "severity": "High",
            "description": (
                "Invoice amount exceeds the policy threshold."
            ),
            "detected_at": "2026-08-27T10:03:00",
            "status": "Open"
        },
        {
            "exception_id": "EXC-VENDOR-INV-013",
            "invoice_id": "INV-013",
            "exception_type": "Vendor Anomaly",
            "severity": "High",
            "description": (
                "Invoice is associated with a high-risk vendor."
            ),
            "detected_at": "2026-08-27T10:04:00",
            "status": "Open"
        }
    ]

    # ---------------------------------------------------------
    # 6. Convert dictionaries into ExceptionRecord objects
    # ---------------------------------------------------------
    exceptions = [
        ExceptionRecord(**exception)
        for exception in exception_data
    ]

    # ---------------------------------------------------------
    # 7. Risk Assessment
    # ---------------------------------------------------------
    risk_result = {
        "invoice_id": "INV-013",
        "risk_score": 100,
        "risk_level": "Critical",
        "risk_factors": [
            "Amount Mismatch",
            "Missing Approval",
            "Quantity Mismatch",
            "Policy Violation",
            "Vendor Anomaly"
        ],
        "explanation": (
            "Invoice has 5 detected exception(s) "
            "with a combined risk score of 100."
        )
    }

    # ---------------------------------------------------------
    # 8. Payment Recommendation
    # ---------------------------------------------------------
    recommendation = {
        "recommendation_id": "REC-INV-013",
        "invoice_id": "INV-013",
        "action": "Block Payment",
        "priority": "Critical",
        "reason": (
            "Multiple financial control violations "
            "were detected."
        ),
        "requires_human_review": True
    }

    # ---------------------------------------------------------
    # 9. Build Evidence
    # ---------------------------------------------------------
    evidence_list = []

    for exception in exceptions:

        exception_type = exception.exception_type

        if exception_type == "Amount Mismatch":

            evidence_list.append(
                build_evidence(
                    exception=exception,
                    source_type="Purchase Order",
                    source_reference="PO-013",
                    description=(
                        "Invoice amount is ₹75,000, "
                        "while the approved purchase order "
                        "amount is ₹50,000."
                    ),
                    confidence=1.0
                )
            )

        elif exception_type == "Missing Approval":

            evidence_list.append(
                build_evidence(
                    exception=exception,
                    source_type="Approval Records",
                    source_reference="INV-013",
                    description=(
                        "No approval record was found "
                        "for invoice INV-013."
                    ),
                    confidence=1.0
                )
            )

        elif exception_type == "Quantity Mismatch":

            evidence_list.append(
                build_evidence(
                    exception=exception,
                    source_type="Goods Receipt",
                    source_reference="REC-013",
                    description=(
                        "Invoice quantity is 100, "
                        "while received quantity is 80."
                    ),
                    confidence=1.0
                )
            )

        elif exception_type == "Policy Violation":

            evidence_list.append(
                build_evidence(
                    exception=exception,
                    source_type="Financial Policy",
                    source_reference="POLICY-001",
                    description=(
                        "Invoice amount exceeds the applicable "
                        "financial control threshold."
                    ),
                    confidence=0.95
                )
            )

        elif exception_type == "Vendor Anomaly":

            evidence_list.append(
                build_evidence(
                    exception=exception,
                    source_type="Vendor Master",
                    source_reference="V-002",
                    description=(
                        "Vendor XYZ Traders is classified "
                        "as a high-risk vendor."
                    ),
                    confidence=0.95
                )
            )

    # ---------------------------------------------------------
    # 10. Build ordered evidence chain
    # ---------------------------------------------------------
    evidence = build_evidence_chain(evidence_list)

    # ---------------------------------------------------------
    # 11. Run Investigation Engine
    # ---------------------------------------------------------
    investigation = investigate_invoice(
        invoice=invoice,
        exceptions=exceptions,
        risk_result=risk_result,
        recommendation=recommendation
    )

    # ---------------------------------------------------------
    # 12. Return Investigation Result
    # ---------------------------------------------------------
    return {
        "invoice": invoice,
        "purchase_order": purchase_order,
        "receipt": receipt,
        "vendor": vendor,

        "exceptions": [
            exception.model_dump()
            for exception in exceptions
        ],

        "risk_result": risk_result,

        "recommendation": recommendation,

        "investigation": investigation,

        "evidence": [
            evidence_item.model_dump()
            for evidence_item in evidence
        ]
    }
