from pydantic import BaseModel
from datetime import datetime


class ExceptionRecord(BaseModel):
    exception_id: str
    invoice_id: str
    exception_type: str
    severity: str
    description: str
    detected_at: datetime
    status: str