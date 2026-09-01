from typing import Dict, Any

from app.investigation.root_cause import identify_root_causes


def investigate_invoice(
    invoice: Dict[str, Any],
    exceptions: list,
    risk_result: Dict[str, Any],
    recommendation: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Investigates an invoice using detected exceptions,
    risk assessment, and recommendation.
    """

    # Get exception types from Pydantic ExceptionRecord objects
    exception_types = [
        exception.exception_type
        for exception in exceptions
    ]

    # Count high and critical risk exceptions
    high_risk_exceptions = [
        exception
        for exception in exceptions
        if exception.severity in ["High", "Critical"]
    ]

    # Determine likely root causes
    root_causes = identify_root_causes(exceptions)

    # Risk information
    risk_level = risk_result.get("risk_level", "Unknown")
    risk_score = risk_result.get("risk_score", 0)

    # Investigation conclusion
    if risk_level == "Critical":
        conclusion = (
            "The invoice presents critical financial control risks "
            "and should not be paid until the identified issues are reviewed."
        )

    elif risk_level == "High":
        conclusion = (
            "The invoice presents significant financial control risks "
            "and requires human review."
        )

    elif risk_level == "Medium":
        conclusion = (
            "The invoice contains moderate control concerns "
            "that should be reviewed before payment."
        )

    else:
        conclusion = (
            "No critical financial control concerns were identified."
        )

    return {
        "invoice_id": invoice.get("invoice_id"),
        "investigation_status": "Completed",
        "risk_score": risk_score,
        "risk_level": risk_level,
        "exceptions_count": len(exceptions),
        "high_risk_exceptions": len(high_risk_exceptions),
        "root_causes": root_causes,
        "detected_exceptions": exception_types,
        "recommended_action": recommendation.get(
            "action",
            "No action available"
        ),
        "human_review_required": recommendation.get(
            "requires_human_review",
            True
        ),
        "conclusion": conclusion
    }
