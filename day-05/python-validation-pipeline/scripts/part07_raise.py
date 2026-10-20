def validate_quantity(value):
    try:
        quantity = int (value)
    except ValueError:
        raise ValueError("Qunatity must be a whole number")
    if quantity <=0:
        raise ValueError ("Quantity must be a grater than a zero")
    return quantity

test_values = ["5","zero", "0", "-3"]
for value in test_values:
    try:
        result = validate_quantity(value)
        print(f"{value} -> valid:{result}")
    except ValueError as error:
        print(f"{value} -> INVALID: {error}")