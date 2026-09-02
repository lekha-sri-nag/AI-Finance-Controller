from models.exception import ExceptionRecord
from app.investigation.root_cause import identify_root_causes


def create_exception(exception_type):
    return ExceptionRecord(
        exception_id=f"EXC-{exception_type.replace(' ', '-')}",
        invoice_id="INV-TEST-001",
        exception_type=exception_type,
        severity="High",
        description="Test exception",
        detected_at="2026-09-01T10:00:00",
        status="Open"
    )


def test_amount_mismatch_root_cause():
    exceptions = [
        create_exception("Amount Mismatch")
    ]

    root_causes = identify_root_causes(exceptions)

    assert len(root_causes) == 1
    assert "purchase order" in root_causes[0]


def test_multiple_root_causes():
    exceptions = [
        create_exception("Amount Mismatch"),
        create_exception("Quantity Mismatch"),
        create_exception("Missing Approval"),
    ]

    root_causes = identify_root_causes(exceptions)

    assert len(root_causes) == 3


def test_no_exceptions_root_cause():
    root_causes = identify_root_causes([])

    assert len(root_causes) == 1
    assert "No significant root cause" in root_causes[0]


def test_duplicate_invoice_root_cause():
    exceptions = [
        create_exception("Duplicate Invoice")
    ]

    root_causes = identify_root_causes(exceptions)

    assert len(root_causes) == 1
    assert "already been processed" in root_causes[0]
