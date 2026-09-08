from io import BytesIO

import fitz


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF document.

    Args:
        pdf_bytes: Raw PDF bytes.

    Returns:
        Extracted text from all PDF pages.
    """

    if not pdf_bytes:
        raise ValueError("PDF data is empty.")

    document = fitz.open(
        stream=BytesIO(pdf_bytes),
        filetype="pdf"
    )

    pages = []

    for page in document:
        text = page.get_text()

        if text.strip():
            pages.append(text.strip())

    document.close()

    return "\n\n".join(pages)