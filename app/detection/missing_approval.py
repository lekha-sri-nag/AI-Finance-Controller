from models.invoice import Invoice
from models.approval import Approval
from models.exception import ExceptionRecord
from datetime import datetime


def detect_missing_approval(
    invoice: Invoice,
    approvals: list[Approval]
) -> ExceptionRecord | None:

    invoice_approvals = [
        approval
        for approval in approvals
        if approval.invoice_id == invoice.invoice_id
    ]

    if not invoice_approvals:

        return ExceptionRecord(
            exception_id=f"EXC-APPROVAL-{invoice.invoice_id}",
            invoice_id=invoice.invoice_id,
            exception_type="Missing Approval",
            severity="High",
            description=(
                f"Invoice {invoice.invoice_id} has no approval record."
            ),
            detected_at=datetime.now(),
            status="Open"
        )

    return None