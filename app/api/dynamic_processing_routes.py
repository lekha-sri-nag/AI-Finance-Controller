from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import require_roles
from app.database.models import User
from app.services.dynamic_processor import process_invoice_from_data


router = APIRouter()

UPLOAD_DIR = Path("data/uploads")


@router.post("/invoices/{invoice_id}/process-from-data")
def process_invoice_from_data_endpoint(
    invoice_id: str,
    file_name: str,
    current_user: User = Depends(
        require_roles("admin", "finance_controller")
    )
):
    """
    Process an invoice using the uploaded invoice file.

    Only Admin and Finance Controller users can
    trigger invoice processing.
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