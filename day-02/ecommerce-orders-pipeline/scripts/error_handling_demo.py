
try:
    number = int(input("Enter a number: "))
    result = 100 / number
    print("Result:", result)

except ValueError:
    print("ERROR: Please enter a valid number.")

except ZeroDivisionError:
    print("ERROR: Number cannot be zero.")

else:
    print("Calculation completed successfully.")

finally:
    print("Program finished.")
