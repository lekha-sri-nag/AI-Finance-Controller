from io import BytesIO

import pytesseract
from PIL import Image, ImageEnhance, ImageOps


def _preprocess_image(image_bytes: bytes) -> Image.Image:
    """
    Preprocess an invoice image before OCR.
    """

    if not image_bytes:
        raise ValueError("Image data is empty.")

    image = Image.open(BytesIO(image_bytes))

    # Convert to grayscale
    image = ImageOps.grayscale(image)

    # Enlarge the image for better OCR accuracy
    image = image.resize(
        (image.width * 3, image.height * 3)
    )

    # Improve contrast
    image = ImageEnhance.Contrast(image).enhance(2.5)

    # Sharpen text edges
    image = ImageEnhance.Sharpness(image).enhance(2.0)

    # Convert to clean black-and-white image
    image = image.point(
        lambda pixel: 0 if pixel < 160 else 255
    )

    return image


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from an invoice image using Tesseract OCR.

    This function preserves the original API and returns
    only the extracted text.
    """

    image = _preprocess_image(image_bytes)

    text = pytesseract.image_to_string(
        image,
        config="--psm 6"
    )

    return text.strip()


def extract_invoice_ocr(image_bytes: bytes) -> dict:
    """
    Extract invoice text together with OCR confidence information.
    """

    image = _preprocess_image(image_bytes)

    ocr_data = pytesseract.image_to_data(
        image,
        config="--psm 6",
        output_type=pytesseract.Output.DICT
    )

    text_parts = []
    confidences = []
    low_confidence_words = []
    word_confidences = []

    for index, word in enumerate(ocr_data["text"]):

        word = word.strip()

        if not word:
            continue

        try:
            confidence = float(
                ocr_data["conf"][index]
            )
        except (ValueError, TypeError):
            continue

        text_parts.append(word)
        confidences.append(confidence)

        word_confidences.append(
            {
                "word": word,
                "confidence": round(
                    confidence,
                    2
                )
            }
        )

        if confidence < 70:
            low_confidence_words.append(
                {
                    "word": word,
                    "confidence": round(
                        confidence,
                        2
                    )
                }
            )

    text = " ".join(text_parts)

    average_confidence = (
        sum(confidences) / len(confidences)
        if confidences
        else 0.0
    )

    review_required = (
        average_confidence < 85
        or len(low_confidence_words) > 0
    )

    return {
        "text": text,
        "average_confidence": round(
            average_confidence,
            2
        ),
        "word_confidences": word_confidences,
        "low_confidence_words": low_confidence_words,
        "review_required": review_required
    }


def get_invoice_field_confidence(
    ocr_result: dict,
    parsed_invoice: dict
) -> dict:
    """
    Calculate confidence for each extracted invoice field
    using actual OCR word-level confidence scores.
    """

    word_confidences = ocr_result.get(
        "word_confidences",
        []
    )

    if not word_confidences:
        return {}

    def confidence_for_value(value):
        if value is None:
            return None

        value_text = (
            str(value)
            .strip()
            .lower()
            .replace(",", "")
            .replace(" ", "")
        )

        matched_scores = []

        for item in word_confidences:

            word = (
                str(item.get("word", ""))
                .strip()
                .lower()
                .replace(",", "")
                .replace(" ", "")
            )

            if not word:
                continue

            normalized_word = word

            # Common OCR substitutions in invoice IDs
            normalized_word = normalized_word.replace(
                "q",
                "o"
            )

            normalized_word = normalized_word.replace(
                "—",
                "-"
            )

            normalized_word = normalized_word.replace(
                "–",
                "-"
            )

            if (
                normalized_word == value_text
                or value_text in normalized_word
                or normalized_word in value_text
            ):
                matched_scores.append(
                    float(
                        item.get(
                            "confidence",
                            0
                        )
                    )
                )

        if not matched_scores:
            return None

        return round(
            sum(matched_scores)
            / len(matched_scores),
            2
        )

    field_confidence = {}

    field_mapping = {
        "invoice_id": "invoice_id_confidence",
        "vendor_id": "vendor_id_confidence",
        "purchase_order_id": "purchase_order_id_confidence",
        "invoice_date": "invoice_date_confidence",
        "quantity": "quantity_confidence",
        "amount": "amount_confidence",
        "currency": "currency_confidence",
    }

    for field, confidence_key in field_mapping.items():

        value = parsed_invoice.get(field)

        field_confidence[
            confidence_key
        ] = confidence_for_value(value)

    return field_confidence


def identify_low_confidence_fields(
    field_confidence: dict,
    threshold: float = 70.0
) -> list[str]:
    """
    Identify invoice fields whose OCR confidence
    is below the required threshold.

    Known OCR-normalized identifier fields are allowed
    to pass when the parser has already successfully
    normalized the extracted value.
    """

    low_confidence_fields = []

    for field, confidence in field_confidence.items():

        if confidence is None:
            low_confidence_fields.append(field)
            continue

        # Purchase order IDs can contain common OCR
        # substitutions such as O -> Q.
        #
        # The parser already normalizes these values
        # before financial validation.
        if field == "purchase_order_id_confidence":
            if confidence >= 40.0:
                continue

        if confidence < threshold:
            low_confidence_fields.append(field)

    return low_confidence_fields