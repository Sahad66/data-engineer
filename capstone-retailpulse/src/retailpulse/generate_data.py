
from pathlib import Path

import pandas as pd


# Project root: capstone-retailpulse
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Fixed seed makes the generated data reproducible.
SEED = 42


def generate_data():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    customers = pd.DataFrame(
        [
            {"customer_id": "C001", "customer_name": "Amina", "city": "Dhaka"},
            {"customer_id": "C002", "customer_name": "Rahim", "city": "Rajshahi"},
            {"customer_id": "C003", "customer_name": "Nadia", "city": "Chattogram"},
            {"customer_id": "C004", "customer_name": "Hasan", "city": "Khulna"},
            {"customer_id": "C005", "customer_name": "Mitu", "city": "Sylhet"},
        ]
    )

    products = pd.DataFrame(
        [
            {"product_id": "P001", "product_name": "Keyboard", "category": "Electronics", "unit_price": 1200.00},
            {"product_id": "P002", "product_name": "Mouse", "category": "Electronics", "unit_price": 650.00},
            {"product_id": "P003", "product_name": "Notebook", "category": "Stationery", "unit_price": 120.00},
            {"product_id": "P004", "product_name": "Backpack", "category": "Accessories", "unit_price": 950.00},
            {"product_id": "P005", "product_name": "Water Bottle", "category": "Accessories", "unit_price": 350.00},
        ]
    )

    orders = pd.DataFrame(
        [
            {"order_id": "O1001", "customer_id": "C001", "order_date": "2026-10-01", "product_id": "P001", "quantity": 1},
            {"order_id": "O1002", "customer_id": "C002", "order_date": "2026-10-02", "product_id": "P003", "quantity": 3},
            {"order_id": "O1003", "customer_id": "C003", "order_date": "2026-10-03", "product_id": "P002", "quantity": 2},
            {"order_id": "O1004", "customer_id": "C001", "order_date": "2026-10-04", "product_id": "P004", "quantity": 1},
            {"order_id": "O1005", "customer_id": "C005", "order_date": "2026-10-05", "product_id": "P005", "quantity": 2},
            {"order_id": "O1006", "customer_id": "C004", "order_date": "2026-10-06", "product_id": "P001", "quantity": 1},
            {"order_id": "O1007", "customer_id": "C002", "order_date": "2026-10-07", "product_id": "P004", "quantity": 2},
            {"order_id": "O1008", "customer_id": "C003", "order_date": "2026-10-08", "product_id": "P003", "quantity": 4},
            {"order_id": "O1009", "customer_id": "C005", "order_date": "2026-10-09", "product_id": "P002", "quantity": 1},
            {"order_id": "O1010", "customer_id": "C004", "order_date": "2026-10-10", "product_id": "P005", "quantity": 3},
        ]
    )

    payments = pd.DataFrame(
        [
            {"payment_id": "PAY001", "order_id": "O1001", "payment_method": "card", "payment_status": "paid", "amount": 1200.00},
            {"payment_id": "PAY002", "order_id": "O1002", "payment_method": "mobile_banking", "payment_status": "paid", "amount": 360.00},
            {"payment_id": "PAY003", "order_id": "O1003", "payment_method": "card", "payment_status": "paid", "amount": 1300.00},
            {"payment_id": "PAY004", "order_id": "O1004", "payment_method": "cash", "payment_status": "pending", "amount": 950.00},
            {"payment_id": "PAY005", "order_id": "O1005", "payment_method": "mobile_banking", "payment_status": "paid", "amount": 700.00},
            {"payment_id": "PAY006", "order_id": "O1006", "payment_method": "card", "payment_status": "paid", "amount": 1200.00},
            {"payment_id": "PAY007", "order_id": "O1007", "payment_method": "cash", "payment_status": "paid", "amount": 1900.00},
            {"payment_id": "PAY008", "order_id": "O1008", "payment_method": "mobile_banking", "payment_status": "failed", "amount": 480.00},
            {"payment_id": "PAY009", "order_id": "O1009", "payment_method": "card", "payment_status": "paid", "amount": 650.00},
            {"payment_id": "PAY010", "order_id": "O1010", "payment_method": "cash", "payment_status": "paid", "amount": 1050.00},
        ]
    )

    datasets = {
        "customers.csv": customers,
        "products.csv": products,
        "orders.csv": orders,
        "payments.csv": payments,
    }

    for filename, dataframe in datasets.items():
        output_path = RAW_DATA_DIR / filename
        dataframe.to_csv(output_path, index=False)
        print(f"Created {filename}: {len(dataframe)} rows")

    print("\nDataset generation completed.")


if __name__ == "__main__":
    generate_data()
