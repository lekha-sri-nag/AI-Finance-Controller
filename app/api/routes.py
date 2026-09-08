from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth.dependencies import require_roles
from app.database.models import User

from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from models.receipt import Receipt
from models.policy import Policy
from models.vendor import Vendor

from app.controller import process_invoice


router = APIRouter()


class InvoiceProcessRequest(BaseModel):
    invoice: Invoice
    purchase_order: PurchaseOrder
    receipt: Receipt
    policy: Policy
    vendor: Vendor


@router.get("/invoices/test")
def test_invoice_endpoint():
    return {
        "message": "Invoice processing API is ready"
    }


@router.post("/invoices/process")
def process_invoice_endpoint(
    request: InvoiceProcessRequest,
    current_user: User = Depends(
        require_roles("admin", "finance_controller")
    ),
):

    result = process_invoice(
        invoice=request.invoice,
        purchase_order=request.purchase_order,
        receipt=request.receipt,
        approvals=[],
        policy=request.policy,
        vendor=request.vendor,
        existing_invoices=[]
    )

    return result