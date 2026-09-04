from pathlib import Path

from app.ingestion.csv_ingestor import load_csv
from app.ingestion.excel_ingestor import load_excel
from app.data.validator import validate_invoice_records


def load_financial_data(file_path: str) -> list[dict]:
    """
    Load financial data from a supported source.

    Supported formats:
    - CSV
    - Excel (.xlsx)
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Financial data file not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension == ".csv":
        return load_csv(file_path)

    if extension == ".xlsx":
        return load_excel(file_path)

    raise ValueError(
        f"Unsupported file format: {extension}. "
        "Supported formats are .csv and .xlsx."
    )


def load_and_validate_financial_data(file_path: str):
    """
    Load financial data from CSV or Excel and validate it
    against the Invoice model.

    Returns:
        A list of validated Invoice objects.
    """

    records = load_financial_data(file_path)

    return validate_invoice_records(records)