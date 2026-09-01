from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from app.decision.human_decision import create_decision
from app.database.database import get_db
from app.database.repositories import save_decision, get_decisions_by_invoice


router = APIRouter(
    prefix="/decisions",
    tags=["Decisions"]
)


class DecisionRequest(BaseModel):
    invoice_id: str
    recommendation_id: str
    decision: str
    decided_by: str
    comments: str = ""


@router.post("/")
def submit_decision(
    request: DecisionRequest,
    db: Session = Depends(get_db)
):

    try:

        decision_id = (
            f"DEC-{request.invoice_id}-"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        decision = create_decision(
            decision_id=decision_id,
            invoice_id=request.invoice_id,
            recommendation_id=request.recommendation_id,
            decision=request.decision,
            decided_by=request.decided_by,
            comments=request.comments
        )

        saved_decision = save_decision(
            db,
            decision
        )

        return {
            "status": "success",
            "message": "Human decision recorded successfully.",
            "decision": {
                "decision_id": saved_decision.decision_id,
                "invoice_id": saved_decision.invoice_id,
                "recommendation_id": saved_decision.recommendation_id,
                "decision": saved_decision.decision,
                "decided_by": saved_decision.decided_by,
                "decided_at": saved_decision.decided_at,
                "comments": saved_decision.comments
            }
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/{invoice_id}")
def get_invoice_decisions(
    invoice_id: str,
    db: Session = Depends(get_db)
):

    decisions = get_decisions_by_invoice(
        db,
        invoice_id
    )

    return {
        "status": "success",
        "invoice_id": invoice_id,
        "count": len(decisions),
        "decisions": [
            {
                "decision_id": decision.decision_id,
                "recommendation_id": decision.recommendation_id,
                "decision": decision.decision,
                "decided_by": decision.decided_by,
                "decided_at": decision.decided_at,
                "comments": decision.comments
            }
            for decision in decisions
        ]
    }
