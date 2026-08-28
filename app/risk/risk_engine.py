from models.exception import ExceptionRecord
from models.risk_result import RiskResult
from app.risk.risk_factors import calculate_exception_score


def calculate_risk(
    invoice_id: str,
    exceptions: list[ExceptionRecord]
) -> RiskResult:

    total_score = sum(
        calculate_exception_score(exception.severity)
        for exception in exceptions
    )

    risk_score = min(total_score, 100)

    if risk_score >= 70:
        risk_level = "Critical"
    elif risk_score >= 50:
        risk_level = "High"
    elif risk_score >= 25:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    risk_factors = [
        exception.exception_type
        for exception in exceptions
    ]

    if exceptions:
        explanation = (
            f"Invoice has {len(exceptions)} detected exception(s) "
            f"with a combined risk score of {risk_score}."
        )
    else:
        explanation = "No financial control exceptions detected."

    return RiskResult(
        invoice_id=invoice_id,
        risk_score=risk_score,
        risk_level=risk_level,
        risk_factors=risk_factors,
        explanation=explanation
    )