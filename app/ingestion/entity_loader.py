from app.data.loader import load_financial_data

from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from models.receipt import Receipt
from models.approval import Approval
from models.policy import Policy
from models.vendor import Vendor


ENTITY_MODELS = {
    "invoice": Invoice,
    "purchase_order": PurchaseOrder,
    "receipt": Receipt,
    "approval": Approval,
    "policy": Policy,
    "vendor": Vendor,
}


def load_entity(file_path: str, entity_type: str):
    """
    Load and validate a financial entity from CSV or Excel.

    Args:
        file_path: Path to the CSV or Excel file.
        entity_type: Financial entity type.

    Returns:
        A list of validated Pydantic model objects.
    """

    if entity_type not in ENTITY_MODELS:
        raise ValueError(
            f"Unsupported entity type: {entity_type}. "
            f"Supported types: {', '.join(ENTITY_MODELS.keys())}"
        )

    records = load_financial_data(file_path)

    model = ENTITY_MODELS[entity_type]

    return [
        model(**record)
        for record in records
    ]
