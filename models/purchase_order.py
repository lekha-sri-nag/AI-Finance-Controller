from pydantic import BaseModel
from datetime import date


class PurchaseOrder(BaseModel):
    purchase_order_id: str
    vendor_id: str
    order_date: date
    total_amount: float
    currency: str
    status: str