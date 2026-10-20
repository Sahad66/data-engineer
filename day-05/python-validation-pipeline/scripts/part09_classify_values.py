def classify_integer(value):
    # Step 1: Check missing value
    if value is None:
        return "MISSING"

    # Step 2: Check empty text
    if isinstance(value, str) and value.strip() == "":
        return "EMPTY"

    # Step 3: Try converting to integer
    try:
        number = int(value)
        return f"VALID: {number}"

    except (ValueError, TypeError):
        return "INVALID: Expected a whole number"


test_values = [
    None,
    "",
    "   ",
    "1001",
    "zero",
    0
]

for value in test_values:
    result = classify_integer(value)
    print(f"{repr(value)} -> {result}")
