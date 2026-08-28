from pydantic import BaseModel
from datetime import date


class Approval(BaseModel):
    approval_id: str
    invoice_id: str
    approver_id: str
    approval_date: date
    approval_status: str
    comments: str | None = None