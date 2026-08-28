from pydantic import BaseModel
from datetime import datetime


class Decision(BaseModel):
    decision_id: str
    invoice_id: str
    recommendation_id: str
    decision: str
    decided_by: str
    decided_at: datetime
    comments: str | None = None
    