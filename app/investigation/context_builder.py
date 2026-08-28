from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from models.receipt import Receipt
from models.vendor import Vendor
from models.approval import Approval
from models.exception import ExceptionRecord
from models.risk_result import RiskResult
from models.recommendation import Recommendation
from models.evidence import Evidence


def build_investigation_context(
    invoice: Invoice,
    purchase_order: PurchaseOrder,
    receipt: Receipt,
    vendor: Vendor,
    approvals: list[Approval],
    exceptions: list[ExceptionRecord],
    risk_result: RiskResult,
    recommendation: Recommendation,
    evidence: list[Evidence]
) -> dict:

    return {
        "invoice": invoice,
        "purchase_order": purchase_order,
        "receipt": receipt,
        "vendor": vendor,
        "approvals": approvals,
        "exceptions": exceptions,
        "risk_result": risk_result,
        "recommendation": recommendation,
        "evidence": evidence
    }