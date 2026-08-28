from models.evidence import Evidence


def build_evidence_chain(
    evidence_list: list[Evidence]
) -> list[Evidence]:

    return sorted(
        evidence_list,
        key=lambda evidence: evidence.confidence,
        reverse=True
    )