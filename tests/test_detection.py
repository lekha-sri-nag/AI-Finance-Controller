from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from models.receipt import Receipt
from models.approval import Approval
from models.policy import Policy
from models.vendor import Vendor

from app.detection.amount_mismatch import detect_amount_mismatch
from app.detection.quantity_mismatch import detect_quantity_mismatch
from app.detection.missing_approval import detect_missing_approval
from app.detection.policy_violation import detect_policy_violation
from app.detection.vendor_anomaly import detect_vendor_anomaly
from app.detection.duplicate_invoice import detect_duplicate_invoice


def create_invoice():
    return Invoice(
        invoice_id="INV-TEST-001",
        vendor_id="V-TEST",
        purchase_order_id="PO-TEST",
        invoice_date="2026-09-01",
        amount=75000,
        quantity=100,
        currency="INR",
        status="Pending"
    )


def test_amount_mismatch():
    invoice = create_invoice()

    purchase_order = PurchaseOrder(
        purchase_order_id="PO-TEST",
        vendor_id="V-TEST",
        order_date="2026-08-20",
        total_amount=50000,
        currency="INR",
        status="Approved"
    )

    result = detect_amount_mismatch(invoice, purchase_order)

    assert result is not None
    assert result.exception_type == "Amount Mismatch"


def test_quantity_mismatch():
    invoice = create_invoice()

    receipt = Receipt(
        receipt_id="REC-TEST",
        purchase_order_id="PO-TEST",
        receipt_date="2026-09-01",
        quantity_received=80,
        received_amount=40000,
        status="Received"
    )

    result = detect_quantity_mismatch(invoice, receipt)

    assert result is not None
    assert result.exception_type == "Quantity Mismatch"


def test_missing_approval():
    invoice = create_invoice()

    result = detect_missing_approval(
        invoice,
        []
    )

    assert result is not None
    assert result.exception_type == "Missing Approval"


def test_policy_violation():
    invoice = create_invoice()

    policy = Policy(
        policy_id="POLICY-TEST",
        policy_name="Test Financial Policy",
        category="Financial Control",
        description="Test policy",
        threshold_amount=50000,
        approval_required=True,
        active=True
    )

    result = detect_policy_violation(
        invoice,
        policy
    )

    assert result is not None
    assert result.exception_type == "Policy Violation"


def test_vendor_anomaly():
    invoice = create_invoice()

    vendor = Vendor(
        vendor_id="V-TEST",
        vendor_name="Test Vendor",
        tax_id="GST-TEST",
        category="Electronics",
        risk_level="High",
        active=True
    )

    result = detect_vendor_anomaly(
        invoice,
        vendor
    )

    assert result is not None
    assert result.exception_type == "Vendor Anomaly"


def test_duplicate_invoice():
    invoice = create_invoice()

    existing_invoices = [invoice]

    result = detect_duplicate_invoice(
        invoice,
        existing_invoices
    )

    assert result is not None
    assert result.exception_type == "Duplicate Invoice"
