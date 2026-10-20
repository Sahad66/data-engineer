
from pathlib import Path

file_path = Path("data/orders.csv")

print("Pipeline started")

try:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            print(line.strip())

except FileNotFoundError:
    print(f"ERROR: File not found: {file_path}")

except PermissionError:
    print("ERROR: Permission denied while reading file")

else:
    print("File reading completed successfully")

finally:
    print("File operation finished")

print("Pipeline ended")
