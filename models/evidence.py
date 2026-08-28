from pydantic import BaseModel


class Evidence(BaseModel):
    evidence_id: str
    exception_id: str
    source_type: str
    source_reference: str
    description: str
    confidence: float