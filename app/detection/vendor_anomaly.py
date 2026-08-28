from models.invoice import Invoice
from models.vendor import Vendor
from models.exception import ExceptionRecord
from datetime import datetime


def detect_vendor_anomaly(
    invoice: Invoice,
    vendor: Vendor
) -> ExceptionRecord | None:

    if vendor.risk_level.lower() == "high" and vendor.active:

        return ExceptionRecord(
            exception_id=f"EXC-VENDOR-{invoice.invoice_id}",
            invoice_id=invoice.invoice_id,
            exception_type="Vendor Anomaly",
            severity="High",
            description=(
                f"Invoice is associated with high-risk vendor "
                f"{vendor.vendor_id} ({vendor.vendor_name})."
            ),
            detected_at=datetime.now(),
            status="Open"
        )

    return None