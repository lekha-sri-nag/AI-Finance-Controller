from models.decision import Decision
from app.decision.decision_validator import validate_decision
from datetime import datetime


def create_decision(
    decision_id: str,
    invoice_id: str,
    recommendation_id: str,
    decision: str,
    decided_by: str,
    comments: str
) -> Decision:

    if not validate_decision(decision):
        raise ValueError(
            f"Invalid decision: {decision}. "
            f"Allowed decisions are: "
            f"Approve, Reject, Hold, Block."
        )

    return Decision(
        decision_id=decision_id,
        invoice_id=invoice_id,
        recommendation_id=recommendation_id,
        decision=decision,
        decided_by=decided_by,
        decided_at=datetime.now(),
        comments=comments
    )