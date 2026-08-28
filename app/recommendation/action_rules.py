RISK_ACTIONS = {
    "Low": {
        "action": "Approve Payment",
        "priority": "Low",
        "requires_human_review": False
    },
    "Medium": {
        "action": "Review Invoice",
        "priority": "Medium",
        "requires_human_review": True
    },
    "High": {
        "action": "Hold Payment",
        "priority": "High",
        "requires_human_review": True
    },
    "Critical": {
        "action": "Block Payment",
        "priority": "Critical",
        "requires_human_review": True
    }
}


def get_action_for_risk(risk_level: str) -> dict:
    return RISK_ACTIONS.get(
        risk_level,
        RISK_ACTIONS["Medium"]
    )