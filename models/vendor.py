from pydantic import BaseModel


class Vendor(BaseModel):
    vendor_id: str
    vendor_name: str
    tax_id: str
    category: str
    risk_level: str
    active: bool