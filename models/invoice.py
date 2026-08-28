from pydantic import BaseModel
from datetime import date


class Invoice(BaseModel):
    invoice_id: str
    vendor_id: str
    purchase_order_id: str
    invoice_date: date
    amount: float
    quantity: int
    currency: str
    status: str