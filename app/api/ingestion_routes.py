from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ingestion.entity_loader import load_entity


router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/ingestion/invoices")
async def upload_invoices(file: UploadFile = File(...)):
    """
    Upload and validate an invoice CSV or Excel file.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file name provided."
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in {".csv", ".xlsx"}:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel (.xlsx) files are supported."
        )

    file_path = UPLOAD_DIR / file.filename

    try:
        contents = await file.read()
        file_path.write_bytes(contents)

        invoices = load_entity(
            str(file_path),
            "invoice"
        )

        return {
            "message": "Invoice file uploaded and validated successfully.",
            "file_name": file.filename,
            "record_count": len(invoices),
            "invoices": [
                invoice.model_dump(mode="json")
                for invoice in invoices
            ]
        }

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
