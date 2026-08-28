from models.audit_record import AuditRecord
from datetime import datetime


def create_audit_record(
    audit_id: str,
    entity_type: str,
    entity_id: str,
    action: str,
    performed_by: str,
    details: str
) -> AuditRecord:

    return AuditRecord(
        audit_id=audit_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        performed_by=performed_by,
        performed_at=datetime.now(),
        details=details
    )