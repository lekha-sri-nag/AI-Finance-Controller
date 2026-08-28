from models.invoice import Invoice
from models.exception import ExceptionRecord
from datetime import datetime


def detect_duplicate_invoice(
    invoice: Invoice,
    existing_invoices: list[Invoice]
) -> ExceptionRecord | None:

    for existing_invoice in existing_invoices:

        if (
            invoice.invoice_id == existing_invoice.invoice_id
            and invoice.vendor_id == existing_invoice.vendor_id
        ):
            return ExceptionRecord(
                exception_id=f"EXC-DUPLICATE-{invoice.invoice_id}",
                invoice_id=invoice.invoice_id,
                exception_type="Duplicate Invoice",
                severity="High",
                description=(
                    f"Invoice {invoice.invoice_id} already exists "
                    f"for vendor {invoice.vendor_id}."
                ),
                detected_at=datetime.now(),
                status="Open"
            )

    return None