def validate_evidence(evidence) -> bool:

    if not evidence.evidence_id:
        return False

    if not evidence.exception_id:
        return False

    if not evidence.source_type:
        return False

    if not evidence.source_reference:
        return False

    if not evidence.description:
        return False

    if not 0 <= evidence.confidence <= 1:
        return False

    return True