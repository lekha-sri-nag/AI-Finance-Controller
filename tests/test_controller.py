from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from models.receipt import Receipt
from models.policy import Policy
from models.vendor import Vendor

from app.controller import process_invoice


def test_process_invoice_with_exceptions():

    invoice = Invoice(
        invoice_id="INV-CONTROLLER-001",
        vendor_id="V-TEST",
        purchase_order_id="PO-CONTROLLER-001",
        invoice_date="2026-09-01",
        amount=75000,
        quantity=100,
        currency="INR",
        status="Pending"
    )

    purchase_order = PurchaseOrder(
        purchase_order_id="PO-CONTROLLER-001",
        vendor_id="V-TEST",
        order_date="2026-08-20",
        total_amount=50000,
        currency="INR",
        status="Approved"
    )

    receipt = Receipt(
        receipt_id="REC-CONTROLLER-001",
        purchase_order_id="PO-CONTROLLER-001",
        receipt_date="2026-09-01",
        quantity_received=80,
        received_amount=40000,
        status="Received"
    )

    policy = Policy(
        policy_id="POLICY-CONTROLLER-001",
        policy_name="Financial Control Policy",
        category="Financial Control",
        description="Controls invoice approval thresholds.",
        threshold_amount=50000,
        approval_required=True,
        active=True
    )

    vendor = Vendor(
        vendor_id="V-TEST",
        vendor_name="Test Vendor",
        tax_id="GST-CONTROLLER",
        category="Electronics",
        risk_level="High",
        active=True
    )

    result = process_invoice(
        invoice=invoice,
        purchase_order=purchase_order,
        receipt=receipt,
        approvals=[],
        policy=policy,
        vendor=vendor,
        existing_invoices=[]
    )

    assert "invoice" in result
    assert "exceptions" in result
    assert "risk_result" in result
    assert "recommendation" in result

    assert result["invoice"].invoice_id == "INV-CONTROLLER-001"

    assert len(result["exceptions"]) > 0

    assert result["risk_result"].invoice_id == "INV-CONTROLLER-001"
    assert result["risk_result"].risk_level == "Critical"

    assert result["recommendation"].invoice_id == "INV-CONTROLLER-001"
    assert result["recommendation"].action == "Block Payment"
    assert result["recommendation"].requires_human_review is True