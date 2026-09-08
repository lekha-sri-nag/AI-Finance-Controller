from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from app.auth.dependencies import get_current_user, require_roles
from app.database.database import get_db
from app.database.models import User
from app.database.repositories import save_decision, get_decisions_by_invoice
from app.decision.human_decision import create_decision
from app.reporting.excel_report import create_excel_report


router = APIRouter(
    prefix="/decisions",
    tags=["Decisions"]
)


class DecisionRequest(BaseModel):
    invoice_id: str
    recommendation_id: str
    decision: str
    comments: str = ""


@router.post("/")
def submit_decision(
    request: DecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "finance_controller")
    )
):
    try:
        decision = create_decision(
            decision_id=f"DEC-{request.invoice_id}-{int(datetime.now().timestamp())}",
            invoice_id=request.invoice_id,
            recommendation_id=request.recommendation_id,
            decision=request.decision,
            decided_by=current_user.username,
            comments=request.comments
        )

        saved_decision = save_decision(db, decision)

        # Update the Excel report with the human decision.
        create_excel_report(
            invoices=[],
            exceptions=[],
            risk_results=[],
            recommendations=[],
            decisions=[decision]
        )

        return saved_decision

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


@router.get("/{invoice_id}")
def get_invoice_decisions(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    decisions = get_decisions_by_invoice(
        db,
        invoice_id
    )

    return decisions