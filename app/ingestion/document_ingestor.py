from pathlib import Path

from app.ingestion.ocr_extractor import (
    extract_invoice_ocr,
    extract_text_from_image,
    get_invoice_field_confidence,
    identify_low_confidence_fields,
)
from app.ingestion.pdf_extractor import extract_text_from_pdf
from app.ingestion.invoice_document_parser import (
    parse_invoice_document_text,
)


IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".tiff",
    ".bmp",
}


def extract_text_from_document(
    file_path: str,
    file_bytes: bytes
) -> str:
    """
    Extract text from an invoice document.

    Supported formats:
    - PDF
    - PNG
    - JPG
    - JPEG
    - TIFF
    - BMP

    For PDFs, text is first extracted directly.
    If the PDF contains no selectable text, OCR is used
    on the rendered PDF pages.
    """

    if not file_bytes:
        raise ValueError("Document data is empty.")

    extension = Path(file_path).suffix.lower()

    if extension in IMAGE_EXTENSIONS:
        return extract_text_from_image(file_bytes)

    if extension == ".pdf":
        text = extract_text_from_pdf(file_bytes)

        if text.strip():
            return text

        return _extract_text_from_scanned_pdf(file_bytes)

    raise ValueError(
        f"Unsupported document format: {extension}. "
        "Supported formats are PDF and image files."
    )


def extract_invoice_document(
    file_path: str,
    file_bytes: bytes
) -> dict:
    """
    Extract and analyze an invoice document.

    Returns:
    - OCR text
    - parsed invoice fields
    - OCR confidence
    - field-level confidence
    - low-confidence fields
    - human-review requirement
    """

    if not file_bytes:
        raise ValueError("Document data is empty.")

    extension = Path(file_path).suffix.lower()

    if extension in IMAGE_EXTENSIONS:

        ocr_result = extract_invoice_ocr(
            file_bytes
        )

        text = ocr_result["text"]

    elif extension == ".pdf":

        text = extract_text_from_pdf(
            file_bytes
        )

        if text.strip():

            ocr_result = {
                "text": text,
                "average_confidence": None,
                "word_confidences": [],
                "low_confidence_words": [],
                "review_required": False,
            }

        else:
            ocr_result = _extract_ocr_from_scanned_pdf(
                file_bytes
            )

        text = ocr_result["text"]

    else:

        raise ValueError(
            f"Unsupported document format: {extension}. "
            "Supported formats are PDF and image files."
        )

    if not text.strip():
        raise ValueError(
            "No text could be extracted from the invoice document."
        )

    parsed_invoice = parse_invoice_document_text(
        text
    )

    field_confidence = get_invoice_field_confidence(
        ocr_result,
        parsed_invoice
    )

    low_confidence_fields = (
        identify_low_confidence_fields(
            field_confidence
        )
    )

    review_required = (
        (
            ocr_result.get("average_confidence", 0) is not None
            and ocr_result.get("average_confidence", 0) < 85
        )
        or bool(low_confidence_fields)
        or not parsed_invoice.get(
            "extraction_complete",
            False
        )
    )

    return {
        "file_name": Path(file_path).name,
        "text": text,
        "parsed_invoice": parsed_invoice,
        "average_confidence": ocr_result.get(
            "average_confidence"
        ),
        "field_confidence": field_confidence,
        "low_confidence_fields": (
            low_confidence_fields
        ),
        "review_required": review_required,
        "extraction_complete": (
            parsed_invoice.get(
                "extraction_complete",
                False
            )
        ),
    }


def _extract_text_from_scanned_pdf(
    pdf_bytes: bytes
) -> str:
    """
    Render scanned PDF pages as images and extract text using OCR.
    """

    import fitz

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []

    for page in document:

        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        image_bytes = pixmap.tobytes(
            "png"
        )

        text = extract_text_from_image(
            image_bytes
        )

        if text.strip():
            pages.append(
                text.strip()
            )

    document.close()

    return "\n\n".join(pages)


def _extract_ocr_from_scanned_pdf(
    pdf_bytes: bytes
) -> dict:
    """
    Extract OCR text and confidence information
    from every page of a scanned PDF.
    """

    import fitz

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []
    word_confidences = []
    low_confidence_words = []
    confidences = []

    for page in document:

        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        image_bytes = pixmap.tobytes(
            "png"
        )

        page_ocr = extract_invoice_ocr(
            image_bytes
        )

        page_text = page_ocr.get(
            "text",
            ""
        )

        if page_text.strip():
            pages.append(
                page_text.strip()
            )

        word_confidences.extend(
            page_ocr.get(
                "word_confidences",
                []
            )
        )

        low_confidence_words.extend(
            page_ocr.get(
                "low_confidence_words",
                []
            )
        )

        for item in page_ocr.get(
            "word_confidences",
            []
        ):
            try:
                confidences.append(
                    float(
                        item.get(
                            "confidence",
                            0
                        )
                    )
                )
            except (
                ValueError,
                TypeError
            ):
                continue

    document.close()

    text = "\n\n".join(pages)

    average_confidence = (
        sum(confidences) / len(confidences)
        if confidences
        else 0.0
    )

    return {
        "text": text,
        "average_confidence": round(
            average_confidence,
            2
        ),
        "word_confidences": word_confidences,
        "low_confidence_words": low_confidence_words,
        "review_required": (
            average_confidence < 85
            or bool(low_confidence_words)
        ),
    }
