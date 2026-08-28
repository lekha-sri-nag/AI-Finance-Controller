from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from models.exception import ExceptionRecord
from datetime import datetime


def detect_amount_mismatch(
    invoice: Invoice,
    purchase_order: PurchaseOrder
) -> ExceptionRecord | None:

    if invoice.amount != purchase_order.total_amount:

        difference = invoice.amount - purchase_order.total_amount

        return ExceptionRecord(
            exception_id=f"EXC-AMOUNT-{invoice.invoice_id}",
            invoice_id=invoice.invoice_id,
            exception_type="Amount Mismatch",
            severity="High",
            description=(
                f"Invoice amount is {invoice.amount} {invoice.currency}, "
                f"but purchase order amount is "
                f"{purchase_order.total_amount} {purchase_order.currency}. "
                f"Difference: {difference} {invoice.currency}."
            ),
            detected_at=datetime.now(),
            status="Open"
        )

    return None