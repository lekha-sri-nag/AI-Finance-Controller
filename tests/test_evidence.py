from models.exception import ExceptionRecord
from app.evidence.evidence_builder import build_evidence
from app.evidence.evidence_validator import validate_evidence


def create_exception():
    return ExceptionRecord(
        exception_id="EXC-TEST-001",
        invoice_id="INV-TEST-001",
        exception_type="Amount Mismatch",
        severity="High",
        description="Invoice amount exceeds purchase order amount.",
        detected_at="2026-09-01T10:00:00",
        status="Open"
    )


def test_build_evidence():
    exception = create_exception()

    evidence = build_evidence(
        exception=exception,
        source_type="Purchase Order",
        source_reference="PO-TEST-001",
        description="Purchase order shows a lower approved amount.",
        confidence=0.95
    )

    assert evidence.evidence_id == "EVD-EXC-TEST-001"
    assert evidence.exception_id == "EXC-TEST-001"
    assert evidence.source_type == "Purchase Order"
    assert evidence.source_reference == "PO-TEST-001"
    assert evidence.confidence == 0.95


def test_validate_valid_evidence():
    exception = create_exception()

    evidence = build_evidence(
        exception=exception,
        source_type="Purchase Order",
        source_reference="PO-TEST-001",
        description="Purchase order evidence.",
        confidence=0.95
    )

    assert validate_evidence(evidence) is True


def test_validate_missing_source_reference():
    exception = create_exception()

    evidence = build_evidence(
        exception=exception,
        source_type="Purchase Order",
        source_reference="",
        description="Purchase order evidence.",
        confidence=0.95
    )

    assert validate_evidence(evidence) is False


def test_validate_invalid_confidence():
    exception = create_exception()

    evidence = build_evidence(
        exception=exception,
        source_type="Purchase Order",
        source_reference="PO-TEST-001",
        description="Purchase order evidence.",
        confidence=1.5
    )

    assert validate_evidence(evidence) is False