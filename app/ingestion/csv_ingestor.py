import csv
from pathlib import Path


def load_csv(file_path: str) -> list[dict]:
    """
    Load financial records from a CSV file.

    Returns:
        A list of dictionaries representing the CSV records.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported by this loader.")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file does not contain a header row.")

        records = list(reader)

    return records
