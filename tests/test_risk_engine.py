from models.exception import ExceptionRecord
from app.risk.risk_engine import calculate_risk


def test_critical_risk_score():
    invoice_id = "INV-TEST-001"

    exceptions = [
        ExceptionRecord(
            exception_id="EXC-1",
            invoice_id=invoice_id,
            exception_type="Amount Mismatch",
            severity="High",
            description="Test amount mismatch",
            detected_at="2026-09-01T10:00:00",
            status="Open"
        ),
        ExceptionRecord(
            exception_id="EXC-2",
            invoice_id=invoice_id,
            exception_type="Missing Approval",
            severity="High",
            description="Test missing approval",
            detected_at="2026-09-01T10:01:00",
            status="Open"
        ),
    ]

    result = calculate_risk(
        invoice_id=invoice_id,
        exceptions=exceptions
    )

    assert result.risk_score > 0
    assert result.risk_level in ["High", "Critical"]
