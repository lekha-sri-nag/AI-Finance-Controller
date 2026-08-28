VALID_DECISIONS = {
    "Approve",
    "Reject",
    "Hold",
    "Block"
}


def validate_decision(decision: str) -> bool:
    return decision in VALID_DECISIONS