from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.services.dynamic_processor import process_invoice_from_data


router = APIRouter()

UPLOAD_DIR = Path("data/uploads")


@router.post("/invoices/{invoice_id}/process-from-data")
def process_invoice_from_data_endpoint(
    invoice_id: str,
    file_name: str
):
    """
    Process an invoice using the uploaded invoice file.

    Related purchase orders, receipts, approvals, policies,
    and vendors are loaded from the raw financial datasets.
    """

    file_path = UPLOAD_DIR / file_name

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Uploaded invoice file not found: {file_name}"
        )

    try:
        result = process_invoice_from_data(
            invoice_id=invoice_id,
            invoice_file=str(file_path)
        )

        return {
            "invoice": result["invoice"].model_dump(mode="json"),
            "exceptions": [
                exception.model_dump(mode="json")
                for exception in result["exceptions"]
            ],
            "risk_result": result["risk_result"].model_dump(mode="json"),
            "recommendation": result["recommendation"].model_dump(mode="json"),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )