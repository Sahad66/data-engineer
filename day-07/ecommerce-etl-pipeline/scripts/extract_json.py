import json
from pathlib import Path

file_path = Path("data/orders.json")

with file_path.open("r", encoding="utf-8-sig") as file:
    rows = json.load(file)

print("Total rows:", len(rows))
print("First row:", rows[0])
