from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.auth.dependencies import get_current_user, require_roles
from app.database.database import get_db
from app.database.models import User
from app.database.repositories import (
    save_decision,
    get_decisions_by_invoice,
    save_audit_record,
    get_audit_records_by_entity
)
from app.decision.human_decision import create_decision
from app.reporting.excel_report import create_excel_report
from app.audit.audit_logger import create_audit_record


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
            decision_id=(
                f"DEC-{request.invoice_id}-"
                f"{int(datetime.now().timestamp())}"
            ),
            invoice_id=request.invoice_id,
            recommendation_id=request.recommendation_id,
            decision=request.decision,
            decided_by=current_user.username,
            comments=request.comments
        )

        saved_decision = save_decision(db, decision)

        # Create a persistent audit record for the human decision.
        audit_record = create_audit_record(
            audit_id=f"AUD-{uuid.uuid4()}",
            entity_type="Invoice",
            entity_id=request.invoice_id,
            action="Human Decision",
            performed_by=current_user.username,
            details=(
                f"Finance controller decision: "
                f"{request.decision}. "
                f"Comments: {request.comments}"
            )
        )

        save_audit_record(
            db,
            audit_record
        )

        # Update the Excel report with the human decision.
        create_excel_report(
            invoices=[],
            exceptions=[],
            risk_results=[],
            recommendations=[],
            decisions=[decision]
        )

        return {
            "decision_id": saved_decision.decision_id,
            "invoice_id": saved_decision.invoice_id,
            "recommendation_id": saved_decision.recommendation_id,
            "decision": saved_decision.decision,
            "decided_by": saved_decision.decided_by,
            "decided_at": saved_decision.decided_at,
            "comments": saved_decision.comments
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

@router.get("/report/excel")
def download_excel_report(
    current_user: User = Depends(get_current_user)
):
    report_file = Path(
        "data/reports/financial_analysis_report.xlsx"
    )

    if not report_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Excel report not found."
        )

    return FileResponse(
        path=report_file,
        filename="financial_analysis_report.xlsx",
        media_type=(
            "application/vnd.openxmlformats-officedocument"
            ".spreadsheetml.sheet"
        )
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
@router.get("/{invoice_id}/audit")
def get_invoice_audit(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    audit_records = get_audit_records_by_entity(
        db,
        "Invoice",
        invoice_id
    )

    return audit_records