from pydantic import BaseModel
from datetime import datetime


class AuditRecord(BaseModel):
    audit_id: str
    entity_type: str
    entity_id: str
    action: str
    performed_by: str
    performed_at: datetime
    details: str