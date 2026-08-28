from models.invoice import Invoice
from models.receipt import Receipt
from models.exception import ExceptionRecord
from datetime import datetime


def detect_quantity_mismatch(
    invoice: Invoice,
    receipt: Receipt
) -> ExceptionRecord | None:

    if invoice.quantity != receipt.quantity_received:

        difference = invoice.quantity - receipt.quantity_received

        return ExceptionRecord(
            exception_id=f"EXC-QUANTITY-{invoice.invoice_id}",
            invoice_id=invoice.invoice_id,
            exception_type="Quantity Mismatch",
            severity="High",
            description=(
                f"Invoice quantity is {invoice.quantity}, "
                f"but received quantity is "
                f"{receipt.quantity_received}. "
                f"Difference: {difference}."
            ),
            detected_at=datetime.now(),
            status="Open"
        )

    return None