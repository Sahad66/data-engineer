
from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def validate_data():
    customers = pd.read_csv(RAW_DATA_DIR / "customers.csv")
    products = pd.read_csv(RAW_DATA_DIR / "products.csv")
    orders = pd.read_csv(RAW_DATA_DIR / "orders.csv")
    payments = pd.read_csv(RAW_DATA_DIR / "payments.csv")

    results = []

    def check(name, condition):
        passed = bool(condition)
        results.append(passed)
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")

    print("=== RetailPulse Data Quality Report ===\n")

    # Unique IDs
    check("Unique customer IDs", customers["customer_id"].is_unique)
    check("Unique product IDs", products["product_id"].is_unique)
    check("Unique order IDs", orders["order_id"].is_unique)
    check("Unique payment IDs", payments["payment_id"].is_unique)

    # Required fields
    check(
        "Customer required fields",
        customers[["customer_id", "customer_name", "city"]]
        .notna().all().all(),
    )
    check(
        "Product required fields",
        products[["product_id", "product_name", "category", "unit_price"]]
        .notna().all().all(),
    )
    check(
        "Order required fields",
        orders[
            ["order_id", "customer_id", "order_date", "product_id", "quantity"]
        ].notna().all().all(),
    )
    check(
        "Payment required fields",
        payments[
            ["payment_id", "order_id", "payment_method",
             "payment_status", "amount"]
        ].notna().all().all(),
    )

    # Relationships
    check(
        "Order customer IDs exist",
        orders["customer_id"].isin(customers["customer_id"]).all(),
    )
    check(
        "Order product IDs exist",
        orders["product_id"].isin(products["product_id"]).all(),
    )
    check(
        "Payment order IDs exist",
        payments["order_id"].isin(orders["order_id"]).all(),
    )

    # Numeric values
    check("Order quantities are positive", (orders["quantity"] > 0).all())
    check("Product prices are positive", (products["unit_price"] > 0).all())
    check("Payment amounts are positive", (payments["amount"] > 0).all())

    # Allowed payment statuses
    allowed_statuses = {"paid", "pending", "failed"}
    check(
        "Payment statuses are valid",
        payments["payment_status"].isin(allowed_statuses).all(),
    )

    # Compare each payment against its order line total
    order_totals = orders.merge(
        products[["product_id", "unit_price"]],
        on="product_id",
        how="left",
    )
    order_totals["expected_amount"] = (
        order_totals["quantity"] * order_totals["unit_price"]
    )

    payment_check = payments.merge(
        order_totals[["order_id", "expected_amount"]],
        on="order_id",
        how="left",
    )

    amounts_match = (
        payment_check["amount"] - payment_check["expected_amount"]
    ).abs() < 0.01

    check(
        "Payment amounts match order totals",
        amounts_match.all(),
    )

    passed = sum(results)
    failed = len(results) - passed

    print("\n=== Validation Summary ===")
    print(f"Total checks: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed:
        print("Result: DATA QUALITY CHECKS FAILED")
        return False

    print("Result: ALL DATA QUALITY CHECKS PASSED")
    return True


if __name__ == "__main__":
    success = validate_data()
    if not success:
        sys.exit(1)
