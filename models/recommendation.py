from pydantic import BaseModel


class Recommendation(BaseModel):
    recommendation_id: str
    invoice_id: str
    action: str
    priority: str
    reason: str
    requires_human_review: bool