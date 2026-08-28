from pydantic import BaseModel


class RiskResult(BaseModel):
    invoice_id: str
    risk_score: float
    risk_level: str
    risk_factors: list[str]
    explanation: str