
def convert_quantity(value):
    try:
        quantity = int(value)

        if quantity <= 0:
            return "INVALID: Quantity must be positive"

        return f"VALID: {quantity}"

    except ValueError:
        return "INVALID: Quantity must be a whole number"


print(convert_quantity("5"))
print(convert_quantity("zero"))
print(convert_quantity("0"))
print(convert_quantity("-3"))
