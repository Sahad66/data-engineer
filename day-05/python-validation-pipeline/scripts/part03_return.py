
def check_quantity(quantity):
    if quantity > 0:
        return True
    else:
        return False


orders = [5, 0, -2, 8]

for quantity in orders:
    result = check_quantity(quantity)

    if result:
        print(quantity, "-> VALID")
    else:
        print(quantity, "-> INVALID")
