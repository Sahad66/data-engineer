import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def read_csv(name):
    with (DATA_DIR / name).open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        return list(csv.DictReader(file))

source = read_csv("orders.csv")
clean = read_csv("clean_orders.csv")
rejected = read_csv("rejected_orders.csv")

assert len(source) == len(clean) + len(rejected), (
    "Row reconciliation failed"
)

assert all(row["customer_id"].strip() for row in clean), (
    "Clean data has missing customer IDs"
)

assert all(int(row["quantity"]) > 0 for row in clean), (
    "Clean data has invalid quantities"
)

assert all(float(row["unit_price"]) >= 0 for row in clean), (
    "Clean data has negative prices"
)

assert all(row["rejection_reason"].strip() for row in rejected), (
    "Rejected row has no rejection reason"
)

print("TEST RESULT: PASS")
print("Input:", len(source))
print("Clean:", len(clean))
print("Rejected:", len(rejected))
print("Reconciliation: PASS")
print("Quality checks: PASS")
