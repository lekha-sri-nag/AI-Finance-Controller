from sqlalchemy.orm import Session

from app.database.models import DecisionRecord, AuditRecord


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


def save_audit_record(db: Session, audit_record):
    record = AuditRecord(
        audit_id=audit_record.audit_id,
        entity_type=audit_record.entity_type,
        entity_id=audit_record.entity_id,
        action=audit_record.action,
        performed_by=audit_record.performed_by,
        performed_at=audit_record.performed_at,
        details=audit_record.details
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_audit_records_by_entity(
    db: Session,
    entity_type: str,
    entity_id: str
):
    return (
        db.query(AuditRecord)
        .filter(
            AuditRecord.entity_type == entity_type,
            AuditRecord.entity_id == entity_id
        )
        .order_by(AuditRecord.performed_at.desc())
        .all()
    )