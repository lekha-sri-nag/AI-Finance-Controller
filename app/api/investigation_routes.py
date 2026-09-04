from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.controller import process_invoice
from app.ingestion.entity_loader import load_entity
from app.investigation.investigator import investigate_invoice
from app.evidence.evidence_builder import build_evidence
from app.evidence.evidence_chain import build_evidence_chain


router = APIRouter(
    prefix="/invoices",
    tags=["investigation"]
)

RAW_DATA_DIR = Path("data/raw")
UPLOAD_DIR = Path("data/uploads")


@router.get("/{invoice_id}/investigation")
def get_invoice_investigation(invoice_id: str):
    invoice_file = RAW_DATA_DIR / "invoices.csv"

    uploaded_files = sorted(
        UPLOAD_DIR.glob("*"),
        key=lambda path: path.stat().st_mtime,
        reverse=True
    )

    for file_path in uploaded_files:
        if file_path.suffix.lower() not in {".csv", ".xlsx"}:
            continue
        try:
            test_invoices = load_entity(str(file_path), "invoice")
            if any(
                item.invoice_id == invoice_id
                for item in test_invoices
            ):
                invoice_file = file_path
                break
        except Exception:
            continue

    try:
        invoices = load_entity(
            str(invoice_file), "invoice"
        )
        purchase_orders = load_entity(
            str(RAW_DATA_DIR / "purchase_orders.csv"),
            "purchase_order"
        )
        receipts = load_entity(
            str(RAW_DATA_DIR / "receipts.csv"),
            "receipt"
        )
        approvals = load_entity(
            str(RAW_DATA_DIR / "approvals.csv"),
            "approval"
        )
        policies = load_entity(
            str(RAW_DATA_DIR / "policies.csv"),
            "policy"
        )
        vendors = load_entity(
            str(RAW_DATA_DIR / "vendors.csv"),
            "vendor"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    invoice = next(
        (
            item for item in invoices
            if item.invoice_id == invoice_id
        ),
        None
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail=f"Invoice {invoice_id} not found"
        )

    purchase_order = next(
        (
            item for item in purchase_orders
            if item.purchase_order_id
            == invoice.purchase_order_id
        ),
        None
    )

    if purchase_order is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Purchase order "
                f"{invoice.purchase_order_id} not found"
            )
        )

    receipt = next(
        (
            item for item in receipts
            if item.purchase_order_id
            == invoice.purchase_order_id
        ),
        None
    )

    if receipt is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Receipt not found for purchase order: "
                f"{invoice.purchase_order_id}"
            )
        )

    vendor = next(
        (
            item for item in vendors
            if item.vendor_id == invoice.vendor_id
        ),
        None
    )

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor {invoice.vendor_id} not found"
        )

    policy = next(
        (
            item for item in policies
            if item.active
        ),
        None
    )

    if policy is None:
        raise HTTPException(
            status_code=404,
            detail="No active financial policy found"
        )

    existing_invoices = [
        item for item in invoices
        if item.invoice_id != invoice.invoice_id
    ]

    result = process_invoice(
        invoice=invoice,
        purchase_order=purchase_order,
        receipt=receipt,
        approvals=approvals,
        policy=policy,
        vendor=vendor,
        existing_invoices=existing_invoices
    )

    exceptions = result["exceptions"]
    risk_result = result["risk_result"]
    recommendation = result["recommendation"]

    investigation = investigate_invoice(
        invoice=invoice.model_dump(),
        exceptions=exceptions,
        risk_result=risk_result.__dict__,
        recommendation=recommendation.__dict__
    )

    evidence_list = []

    for exception in exceptions:
        evidence = build_evidence(
            exception=exception,
            source_type="Financial Records",
            source_reference=invoice.invoice_id,
            description=exception.description,
            confidence=1.0
        )
        evidence_list.append(evidence)

    evidence_chain = build_evidence_chain(
        evidence_list
    )

    return {
        "invoice": invoice.model_dump(mode="json"),
        "purchase_order": purchase_order.model_dump(mode="json"),
        "receipt": receipt.__dict__,
        "vendor": vendor.__dict__,
        "exceptions": [
            exception.model_dump(mode="json")
            for exception in exceptions
        ],
        "risk_result": risk_result.__dict__,
        "recommendation": recommendation.__dict__,
        "investigation": investigation,
        "evidence": [
            item.__dict__
            for item in evidence_chain
        ]
    }
