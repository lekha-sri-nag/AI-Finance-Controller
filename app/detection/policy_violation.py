from models.invoice import Invoice
from models.policy import Policy
from models.exception import ExceptionRecord
from datetime import datetime


def detect_policy_violation(
    invoice: Invoice,
    policy: Policy
) -> ExceptionRecord | None:

    if (
        policy.active
        and policy.approval_required
        and invoice.amount > policy.threshold_amount
    ):

        return ExceptionRecord(
            exception_id=f"EXC-POLICY-{invoice.invoice_id}",
            invoice_id=invoice.invoice_id,
            exception_type="Policy Violation",
            severity="High",
            description=(
                f"Invoice amount {invoice.amount} {invoice.currency} "
                f"exceeds policy threshold of "
                f"{policy.threshold_amount} {invoice.currency}."
            ),
            detected_at=datetime.now(),
            status="Open"
        )

    return None