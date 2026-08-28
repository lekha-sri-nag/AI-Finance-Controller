from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from models.receipt import Receipt
from models.approval import Approval
from models.policy import Policy
from models.vendor import Vendor

from app.detection.exception_detector import detect_exceptions
from app.risk.risk_engine import calculate_risk
from app.recommendation.recommendation_engine import generate_recommendation


def process_invoice(
    invoice: Invoice,
    purchase_order: PurchaseOrder,
    receipt: Receipt,
    approvals: list[Approval],
    policy: Policy,
    vendor: Vendor,
    existing_invoices: list[Invoice]
) -> dict:

    # Step 1: Detect exceptions
    exceptions = detect_exceptions(
        invoice,
        purchase_order,
        receipt,
        approvals,
        policy,
        vendor,
        existing_invoices
    )

    # Step 2: Calculate risk
    risk_result = calculate_risk(
        invoice.invoice_id,
        exceptions
    )

    # Step 3: Generate recommendation
    recommendation = generate_recommendation(
        risk_result,
        exceptions
    )

    return {
        "invoice": invoice,
        "exceptions": exceptions,
        "risk_result": risk_result,
        "recommendation": recommendation
    }