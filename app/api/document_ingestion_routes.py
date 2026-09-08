from pathlib import Path
import csv

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.auth.dependencies import require_roles
from app.database.models import User
from app.ingestion.document_ingestor import extract_invoice_document
from app.services.dynamic_processor import process_invoice_record
from models.invoice import Invoice


router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".tiff",
    ".bmp",
}

PROCESSING_ROLES = (
    "admin",
    "finance_controller",
)


def persist_invoice(invoice: Invoice):
    """
    Persist a processed invoice as a CSV record.
    """

    invoice_file = (
        UPLOAD_DIR
        / f"{invoice.invoice_id}_processed.csv"
    )

    fieldnames = [
        "invoice_id",
        "vendor_id",
        "purchase_order_id",
        "invoice_date",
        "amount",
        "quantity",
        "currency",
        "status",
    ]

    with invoice_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerow(
            invoice.model_dump(
                mode="json",
            )
        )

    return invoice_file


@router.post("/ingestion/invoice-document")
async def upload_invoice_document(
    file: UploadFile = File(...),
    current_user: User = Depends(
        require_roles(*PROCESSING_ROLES)
    ),
):
    """
    Upload and analyze a PDF/image invoice.

    Only Admin and Finance Controller users
    can upload invoice documents.

    The document is:

    1. Saved to the uploads directory.
    2. Processed through PDF extraction or OCR.
    3. Parsed into invoice fields.
    4. Analyzed for OCR confidence.
    5. Low-confidence fields are identified.
    6. Human review is requested when required.
    7. The extracted invoice is validated.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file name provided.",
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported document format. "
                "Supported formats: PDF, PNG, JPG, "
                "JPEG, TIFF, BMP."
            ),
        )

    try:
        file_bytes = await file.read()

        if not file_bytes:
            raise ValueError(
                "Uploaded document is empty."
            )

        file_path = (
            UPLOAD_DIR
            / file.filename
        )

        file_path.write_bytes(
            file_bytes
        )

        document_result = extract_invoice_document(
            str(file_path),
            file_bytes,
        )

        extracted_text = document_result[
            "text"
        ]

        parsed_data = document_result[
            "parsed_invoice"
        ]

        field_confidence = document_result[
            "field_confidence"
        ]

        low_confidence_fields = (
            document_result[
                "low_confidence_fields"
            ]
        )

        review_required = document_result[
            "review_required"
        ]

        extraction_complete = (
            document_result[
                "extraction_complete"
            ]
        )

        missing_fields = parsed_data[
            "missing_fields"
        ]

        invoice_data = {
            key: value
            for key, value in parsed_data.items()
            if key not in {
                "missing_fields",
                "extraction_complete",
            }
        }

        invoice = None
        validation_error = None

        if not missing_fields:
            try:
                invoice = Invoice(
                    **invoice_data
                )
            except Exception as exc:
                validation_error = str(exc)

        return {
            "message": (
                "Invoice document analyzed successfully."
            ),
            "file_name": file.filename,
            "extracted_text": extracted_text,
            "parsed_fields": parsed_data,
            "invoice": (
                invoice.model_dump(
                    mode="json",
                )
                if invoice
                else None
            ),
            "validation_success": (
                invoice is not None
            ),
            "validation_error": validation_error,
            "ocr_analysis": {
                "average_confidence": (
                    document_result[
                        "average_confidence"
                    ]
                ),
                "field_confidence": (
                    field_confidence
                ),
                "low_confidence_fields": (
                    low_confidence_fields
                ),
            },
            "extraction_complete": (
                extraction_complete
            ),
            "human_review_required": (
                review_required
            ),
            "processing_status": (
                "HUMAN_REVIEW_REQUIRED"
                if review_required
                else "READY_FOR_PROCESSING"
            ),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                "Document processing failed: "
                f"{exc}"
            ),
        )


@router.post(
    "/invoices/{invoice_id}/process-document"
)
async def process_invoice_document(
    invoice_id: str,
    file_name: str,
    current_user: User = Depends(
        require_roles(*PROCESSING_ROLES)
    ),
):
    """
    Process a previously uploaded PDF/image invoice.

    Low-confidence OCR results are blocked from
    automatic financial processing and require
    human review first.
    """

    file_path = (
        UPLOAD_DIR
        / file_name
    )

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=(
                "Uploaded document not found: "
                f"{file_name}"
            ),
        )

    try:
        file_bytes = file_path.read_bytes()

        document_result = extract_invoice_document(
            str(file_path),
            file_bytes,
        )

        extracted_text = document_result[
            "text"
        ]

        parsed_data = document_result[
            "parsed_invoice"
        ]

        low_confidence_fields = (
            document_result[
                "low_confidence_fields"
            ]
        )

        review_required = document_result[
            "review_required"
        ]

        if review_required:
            raise ValueError(
                "Invoice requires human review "
                "before financial processing. "
                f"Low-confidence fields: "
                f"{low_confidence_fields}"
            )

        if not extracted_text.strip():
            raise ValueError(
                "No readable text could be "
                "extracted from the invoice."
            )

        parsed_invoice_id = parsed_data[
            "invoice_id"
        ]

        if parsed_invoice_id != invoice_id:
            raise ValueError(
                "Invoice ID in the document "
                "does not match the requested "
                "invoice ID."
            )

        missing_fields = parsed_data[
            "missing_fields"
        ]

        if missing_fields:
            raise ValueError(
                "Invoice extraction is incomplete. "
                f"Missing fields: {missing_fields}"
            )

        invoice_data = {
            key: value
            for key, value in parsed_data.items()
            if key not in {
                "missing_fields",
                "extraction_complete",
            }
        }

        invoice = Invoice(
            **invoice_data
        )

        result = process_invoice_record(
            invoice
        )

        persist_invoice(
            invoice
        )

        return {
            "message": (
                "Invoice document processed "
                "successfully."
            ),
            "invoice": (
                result["invoice"].model_dump(
                    mode="json",
                )
            ),
            "exceptions": [
                exception.model_dump(
                    mode="json",
                )
                for exception
                in result["exceptions"]
            ],
            "risk_result": (
                result["risk_result"].model_dump(
                    mode="json",
                )
            ),
            "recommendation": (
                result["recommendation"].model_dump(
                    mode="json",
                )
            ),
            "ocr_analysis": {
                "average_confidence": (
                    document_result[
                        "average_confidence"
                    ]
                ),
                "field_confidence": (
                    document_result[
                        "field_confidence"
                    ]
                ),
                "low_confidence_fields": (
                    low_confidence_fields
                ),
                "human_review_required": (
                    review_required
                ),
            },
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                "Document processing failed: "
                f"{exc}"
            ),
        )
