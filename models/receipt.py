from pydantic import BaseModel
from datetime import date


class Receipt(BaseModel):
    receipt_id: str
    purchase_order_id: str
    receipt_date: date
    quantity_received: int
    received_amount: float
    status: str