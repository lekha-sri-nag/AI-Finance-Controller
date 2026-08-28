from pydantic import BaseModel


class Policy(BaseModel):
    policy_id: str
    policy_name: str
    category: str
    threshold_amount: float
    approval_required: bool
    description: str
    active: bool