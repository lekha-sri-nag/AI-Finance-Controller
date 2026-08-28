SEVERITY_SCORES = {
    "Low": 10,
    "Medium": 20,
    "High": 30,
    "Critical": 40
}


def calculate_exception_score(severity: str) -> int:
    return SEVERITY_SCORES.get(severity, 0)