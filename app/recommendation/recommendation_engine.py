from models.risk_result import RiskResult
from models.exception import ExceptionRecord
from models.recommendation import Recommendation
from app.recommendation.action_rules import get_action_for_risk


def generate_recommendation(
    risk_result: RiskResult,
    exceptions: list[ExceptionRecord]
) -> Recommendation:

    action_details = get_action_for_risk(
        risk_result.risk_level
    )

    if exceptions:
        reason = (
            f"Recommendation based on {len(exceptions)} "
            f"detected exception(s): "
            f"{', '.join(risk_result.risk_factors)}."
        )
    else:
        reason = "No financial control exceptions detected."

    return Recommendation(
        recommendation_id=f"REC-{risk_result.invoice_id}",
        invoice_id=risk_result.invoice_id,
        action=action_details["action"],
        priority=action_details["priority"],
        reason=reason,
        requires_human_review=action_details[
            "requires_human_review"
        ]
    )