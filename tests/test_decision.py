import pytest

from app.decision.human_decision import create_decision


def test_create_approve_decision():
    decision = create_decision(
        decision_id="DEC-TEST-001",
        invoice_id="INV-TEST-001",
        recommendation_id="REC-TEST-001",
        decision="Approve",
        decided_by="finance_reviewer",
        comments="Invoice approved after review."
    )

    assert decision.decision_id == "DEC-TEST-001"
    assert decision.invoice_id == "INV-TEST-001"
    assert decision.recommendation_id == "REC-TEST-001"
    assert decision.decision == "Approve"
    assert decision.decided_by == "finance_reviewer"
    assert decision.comments == "Invoice approved after review."
    assert decision.decided_at is not None


def test_create_hold_decision():
    decision = create_decision(
        decision_id="DEC-TEST-002",
        invoice_id="INV-TEST-002",
        recommendation_id="REC-TEST-002",
        decision="Hold",
        decided_by="finance_reviewer",
        comments="Payment placed on hold."
    )

    assert decision.decision == "Hold"


def test_create_block_decision():
    decision = create_decision(
        decision_id="DEC-TEST-003",
        invoice_id="INV-TEST-003",
        recommendation_id="REC-TEST-003",
        decision="Block",
        decided_by="finance_reviewer",
        comments="Payment blocked due to critical exceptions."
    )

    assert decision.decision == "Block"


def test_invalid_decision():
    with pytest.raises(ValueError):
        create_decision(
            decision_id="DEC-TEST-004",
            invoice_id="INV-TEST-004",
            recommendation_id="REC-TEST-004",
            decision="Invalid",
            decided_by="finance_reviewer",
            comments="Invalid decision."
        )