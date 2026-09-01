from typing import List


def identify_root_causes(exceptions: list) -> List[str]:
    """
    Identify likely root causes from detected invoice exceptions.

    Supports Pydantic ExceptionRecord objects.
    """

    exception_types = [
        exception.exception_type
        for exception in exceptions
    ]

    root_causes = []

    if "Amount Mismatch" in exception_types:
        root_causes.append(
            "Invoice amount does not match the approved purchase order."
        )

    if "Quantity Mismatch" in exception_types:
        root_causes.append(
            "The invoiced quantity is greater than the quantity received."
        )

    if "Missing Approval" in exception_types:
        root_causes.append(
            "Required approval evidence was not found."
        )

    if "Policy Violation" in exception_types:
        root_causes.append(
            "The invoice exceeds an applicable financial control threshold."
        )

    if "Vendor Anomaly" in exception_types:
        root_causes.append(
            "The invoice is associated with a high-risk vendor."
        )

    if "Duplicate Invoice" in exception_types:
        root_causes.append(
            "A similar invoice appears to have already been processed."
        )

    if not root_causes:
        root_causes.append(
            "No significant root cause was identified."
        )

    return root_causes