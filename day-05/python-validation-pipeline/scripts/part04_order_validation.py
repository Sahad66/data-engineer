
def validate_order(order_id, customer_id, quantity):
    if order_id <= 0:
        return "INVALID: Order ID"

    if customer_id is None or customer_id.strip() == "":
        return "INVALID: Customer ID"

    if quantity <= 0:
        return "INVALID: Quantity"

    return "VALID"


print(validate_order(1001, "C101", 2))
print(validate_order(0, "C102", 1))
print(validate_order(1003, "", 3))
print(validate_order(1004, "C104", 0))

print(validate_order(1005, "C105", 10))
print(validate_order(1006, "   ", 4))