from models.exception import ExceptionRecord
from models.evidence import Evidence


def build_evidence(
    exception: ExceptionRecord,
    source_type: str,
    source_reference: str,
    description: str,
    confidence: float
) -> Evidence:

    return Evidence(
        evidence_id=f"EVD-{exception.exception_id}",
        exception_id=exception.exception_id,
        source_type=source_type,
        source_reference=source_reference,
        description=description,
        confidence=confidence
    )