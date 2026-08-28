from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from models.receipt import Receipt
from models.approval import Approval
from models.policy import Policy
from models.vendor import Vendor
from models.exception import ExceptionRecord

from app.detection.amount_mismatch import detect_amount_mismatch
from app.detection.duplicate_invoice import detect_duplicate_invoice
from app.detection.missing_approval import detect_missing_approval
from app.detection.quantity_mismatch import detect_quantity_mismatch
from app.detection.policy_violation import detect_policy_violation
from app.detection.vendor_anomaly import detect_vendor_anomaly


def detect_exceptions(
    invoice: Invoice,
    purchase_order: PurchaseOrder,
    receipt: Receipt,
    approvals: list[Approval],
    policy: Policy,
    vendor: Vendor,
    existing_invoices: list[Invoice]
) -> list[ExceptionRecord]:

    exceptions = []

    amount_exception = detect_amount_mismatch(
        invoice,
        purchase_order
    )

    if amount_exception:
        exceptions.append(amount_exception)

    duplicate_exception = detect_duplicate_invoice(
        invoice,
        existing_invoices
    )

    if duplicate_exception:
        exceptions.append(duplicate_exception)

    approval_exception = detect_missing_approval(
        invoice,
        approvals
    )

    if approval_exception:
        exceptions.append(approval_exception)

    quantity_exception = detect_quantity_mismatch(
        invoice,
        receipt
    )

    if quantity_exception:
        exceptions.append(quantity_exception)

    policy_exception = detect_policy_violation(
        invoice,
        policy
    )

    if policy_exception:
        exceptions.append(policy_exception)

    vendor_exception = detect_vendor_anomaly(
        invoice,
        vendor
    )

    if vendor_exception:
        exceptions.append(vendor_exception)

    return exceptions