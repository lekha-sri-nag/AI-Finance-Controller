from sqlalchemy.orm import Session
from app.database.models import DecisionRecord


def save_decision(db: Session, decision):
    record = DecisionRecord(
        decision_id=decision.decision_id,
        invoice_id=decision.invoice_id,
        recommendation_id=decision.recommendation_id,
        decision=decision.decision,
        decided_by=decision.decided_by,
        decided_at=decision.decided_at,
        comments=decision.comments
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_decisions_by_invoice(db: Session, invoice_id: str):
    return (
        db.query(DecisionRecord)
        .filter(DecisionRecord.invoice_id == invoice_id)
        .order_by(DecisionRecord.decided_at.desc())
        .all()
    )
