from models.invoice import Invoice


def validate_invoice_records(records: list[dict]) -> list[Invoice]:
    """
    Convert raw financial records into validated Invoice objects.

    Pydantic validates and converts fields such as:
    - invoice_date -> date
    - amount -> float
    - quantity -> int
    """

    invoices = []

    for record in records:
        invoice = Invoice(**record)
        invoices.append(invoice)

    return invoices