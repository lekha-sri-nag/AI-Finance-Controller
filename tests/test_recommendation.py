from models.risk_result import RiskResult
from models.exception import ExceptionRecord
from app.recommendation.recommendation_engine import generate_recommendation


def create_risk_result(risk_level):
    return RiskResult(
        invoice_id="INV-TEST-001",
        risk_score={
            "Low": 10,
            "Medium": 40,
            "High": 60,
            "Critical": 100
        }[risk_level],
        risk_level=risk_level,
        risk_factors=["Amount Mismatch"],
        explanation="Test risk result"
    )


def create_exception():
    return ExceptionRecord(
        exception_id="EXC-TEST-001",
        invoice_id="INV-TEST-001",
        exception_type="Amount Mismatch",
        severity="High",
        description="Test exception",
        detected_at="2026-09-01T10:00:00",
        status="Open"
    )


def test_low_risk_recommendation():
    result = generate_recommendation(
        risk_result=create_risk_result("Low"),
        exceptions=[create_exception()]
    )

    assert result.action == "Approve Payment"
    assert result.priority == "Low"
    assert result.requires_human_review is False


def test_medium_risk_recommendation():
    result = generate_recommendation(
        risk_result=create_risk_result("Medium"),
        exceptions=[create_exception()]
    )

    assert result.action == "Review Invoice"
    assert result.priority == "Medium"
    assert result.requires_human_review is True


def test_high_risk_recommendation():
    result = generate_recommendation(
        risk_result=create_risk_result("High"),
        exceptions=[create_exception()]
    )

    assert result.action == "Hold Payment"
    assert result.priority == "High"
    assert result.requires_human_review is True


def test_critical_risk_recommendation():
    result = generate_recommendation(
        risk_result=create_risk_result("Critical"),
        exceptions=[create_exception()]
    )

    assert result.action == "Block Payment"
    assert result.priority == "Critical"
    assert result.requires_human_review is True