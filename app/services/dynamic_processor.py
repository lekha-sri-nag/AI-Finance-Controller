from pathlib import Path

from app.controller import process_invoice
from app.ingestion.entity_loader import load_entity

from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from models.receipt import Receipt
from models.approval import Approval
from models.policy import Policy
from models.vendor import Vendor


RAW_DATA_DIR = Path("data/raw")


def load_all_financial_entities(invoice_file: str | None = None) -> dict:
    """
    Load all financial entities from the data directories.

    If invoice_file is provided, invoices are loaded from that file.
    Otherwise, invoices are loaded from the default raw dataset.
    """

    invoice_path = (
        Path(invoice_file)
        if invoice_file
        else RAW_DATA_DIR / "invoices.csv"
    )

    return {
        "invoices": load_entity(
            str(invoice_path),
            "invoice"
        ),
        "purchase_orders": load_entity(
            str(RAW_DATA_DIR / "purchase_orders.csv"),
            "purchase_order"
        ),
        "receipts": load_entity(
            str(RAW_DATA_DIR / "receipts.csv"),
            "receipt"
        ),
        "approvals": load_entity(
            str(RAW_DATA_DIR / "approvals.csv"),
            "approval"
        ),
        "policies": load_entity(
            str(RAW_DATA_DIR / "policies.csv"),
            "policy"
        ),
        "vendors": load_entity(
            str(RAW_DATA_DIR / "vendors.csv"),
            "vendor"
        ),
    }


def process_invoice_from_data(
    invoice_id: str,
    invoice_file: str
) -> dict:
    """
    Process an invoice from an uploaded CSV or Excel file.

    Related purchase orders, receipts, approvals, policies,
    and vendors are loaded from the raw financial datasets.
    """

    data = load_all_financial_entities(invoice_file)

    invoices: list[Invoice] = data["invoices"]
    purchase_orders: list[PurchaseOrder] = data["purchase_orders"]
    receipts: list[Receipt] = data["receipts"]
    approvals: list[Approval] = data["approvals"]
    policies: list[Policy] = data["policies"]
    vendors: list[Vendor] = data["vendors"]

    invoice = next(
        (
            item
            for item in invoices
            if item.invoice_id == invoice_id
        ),
        None
    )

    if invoice is None:
        raise ValueError(
            f"Invoice not found: {invoice_id}"
        )

    purchase_order = next(
        (
            item
            for item in purchase_orders
            if item.purchase_order_id == invoice.purchase_order_id
        ),
        None
    )

    if purchase_order is None:
        raise ValueError(
            f"Purchase order not found: "
            f"{invoice.purchase_order_id}"
        )

    receipt = next(
        (
            item
            for item in receipts
            if item.purchase_order_id == invoice.purchase_order_id
        ),
        None
    )

    if receipt is None:
        raise ValueError(
            f"Receipt not found for purchase order: "
            f"{invoice.purchase_order_id}"
        )

    vendor = next(
        (
            item
            for item in vendors
            if item.vendor_id == invoice.vendor_id
        ),
        None
    )

    if vendor is None:
        raise ValueError(
            f"Vendor not found: {invoice.vendor_id}"
        )

    policy = next(
        (
            item
            for item in policies
            if item.active
        ),
        None
    )

    if policy is None:
        raise ValueError(
            "No active financial policy found."
        )

    return process_invoice(
        invoice=invoice,
        purchase_order=purchase_order,
        receipt=receipt,
        approvals=approvals,
        policy=policy,
        vendor=vendor,
        existing_invoices=[
            item
            for item in invoices
            if item.invoice_id != invoice.invoice_id
        ]
    )


def process_invoice_from_raw_data(invoice_id: str) -> dict:
    """
    Process an invoice from the default raw invoice dataset.

    This function is kept for backward compatibility.
    """

    return process_invoice_from_data(
        invoice_id=invoice_id,
        invoice_file=str(RAW_DATA_DIR / "invoices.csv")
    )