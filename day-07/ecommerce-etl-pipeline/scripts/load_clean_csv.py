import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_FILE = BASE_DIR / "data" / "clean_orders.csv"


def load_clean_csv():
    with CLEAN_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    print("Loaded clean rows:", len(rows))
    return rows


if __name__ == "__main__":
    rows = load_clean_csv()
    print("Load preparation: SUCCESS")
