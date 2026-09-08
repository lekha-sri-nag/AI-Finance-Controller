import re
from datetime import datetime


def parse_invoice_document_text(text: str) -> dict:
    """
    Extract invoice fields from OCR or PDF text.

    The parser returns extracted values along with
    fields that could not be confidently identified.
    """

    if not text or not text.strip():
        raise ValueError("Invoice document text is empty.")

    normalized_text = text.replace("\r", "\n")

    result = {
        "invoice_id": _extract_invoice_id(normalized_text),
        "vendor_id": _extract_vendor_id(normalized_text),
        "purchase_order_id": _extract_purchase_order_id(normalized_text),
        "invoice_date": _extract_invoice_date(normalized_text),
        "amount": _extract_amount(normalized_text),
        "quantity": _extract_quantity(normalized_text),
        "currency": _extract_currency(normalized_text),
        "status": "Pending",
    }

    missing_fields = [
        field
        for field, value in result.items()
        if value is None
    ]

    result["missing_fields"] = missing_fields
    result["extraction_complete"] = len(missing_fields) == 0

    return result


def _extract_invoice_id(text: str):
    patterns = [
        r"invoice\s*(?:id|number|no\.?|#)\s*[:\.\-]?\s*([A-Z0-9][A-Z0-9\-\.]*)",
    ]

    return _search_patterns(text, patterns)


def _extract_vendor_id(text: str):
    """
    Extract vendor ID from OCR text.

    OCR may introduce spaces or distort the words
    around the vendor label, so multiple patterns
    are used.
    """

    patterns = [
        # Vendor ID: V-001
        r"vendor\s*(?:id|code|number|no\.?)\s*[:\.\-]?\s*([A-Z0-9][A-Z0-9\-\.]*)",

        # Vendor: V-001
        r"vendor\s*[:\.\-]?\s*(V[\-\s]?\d+)",

        # Vendor ID V-001
        r"vendor\s*(?:id|code)\s+(V[\-\s]?\d+)",

        # OCR may separate V and the number
        # Example: Vendor ID: V 001
        r"vendor\s*(?:id|code|number|no\.?)\s*[:\.\-]?\s*([A-Z]+\s*\d+)",
    ]

    value = _search_patterns(text, patterns)

    if value:
        return _normalize_id(value)

    return None


def _extract_purchase_order_id(text: str):
    patterns = [
        r"purchase\s*order\s*(?:id|number|no\.?|#)?\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-\.]*)",
        r"\bP[OQ]\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-\.]*)",
    ]

    value = _search_patterns(text, patterns)

    if value:
        value = _normalize_id(value)

        # Correct common OCR confusion: PQ -> PO
        if value.startswith("PQ-"):
            value = "PO-" + value[3:]

        return value

    return None


def _extract_invoice_date(text: str):
    patterns = [
        r"invoice\s*date\s*[:\.\-]?\s*(\d{4}[-/]\d{2}[-/]\d{2})",
        r"date\s*[:\.\-]?\s*(\d{4}[-/]\d{2}[-/]\d{2})",
    ]

    value = _search_patterns(text, patterns)

    if not value:
        return None

    value = value.replace("/", "-")

    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        return None


def _extract_amount(text: str):
    patterns = [
        r"(?:total\s*amount|total|grand\s*total|amount)\s*[:\-]?\s*(?:INR|₹|Rs\.?)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"(?:INR|₹|Rs\.?)\s*([\d,]+(?:\.\d{1,2})?)",
    ]

    value = _search_patterns(text, patterns)

    if not value:
        return None

    try:
        return float(value.replace(",", ""))
    except ValueError:
        return None


def _extract_quantity(text: str):
    patterns = [
        r"quantity\s*[:\.\-]?\s*(\d+)",
        r"qty\s*[:\.\-]?\s*(\d+)",
    ]

    value = _search_patterns(text, patterns)

    if not value:
        return None

    try:
        return int(value)
    except ValueError:
        return None


def _extract_currency(text: str):
    if re.search(r"\bINR\b|₹|\bRs\.?", text, re.IGNORECASE):
        return "INR"

    if re.search(r"\bUSD\b|\$", text, re.IGNORECASE):
        return "USD"

    if re.search(r"\bEUR\b|€", text, re.IGNORECASE):
        return "EUR"

    return None


def _search_patterns(text: str, patterns: list[str]):
    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return None


def _normalize_id(value: str):
    value = value.upper().strip()

    # Remove spaces inside IDs such as V 001
    value = re.sub(r"\s+", "", value)

    value = value.replace(".", "-")

    if re.fullmatch(r"\d+", value):
        return value

    return value
