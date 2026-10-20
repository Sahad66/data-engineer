
import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "data" / "orders.json"

try:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Expected a JSON array of orders")

    print("JSON validation: PASS")
    print("Records:", len(data))

except FileNotFoundError:
    print("ERROR: JSON file not found")

except json.JSONDecodeError as error:
    print("ERROR: Invalid JSON")
    print("Line:", error.lineno, "Column:", error.colno)

except ValueError as error:
    print("ERROR:", error)
