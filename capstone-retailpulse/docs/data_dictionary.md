# RetailPulse — Data Dictionary

## Project Overview

RetailPulse is a portfolio project that demonstrates an e-commerce data engineering workflow using synthetic data.

**Source type:** Synthetic CSV data generated locally with Python  
**Data location:** `data/raw/`  
**Validation script:** `src/retailpulse/validate_data.py`

## 1. customers.csv

| Column | Meaning | Expected Rule |
|---|---|---|
| customer_id | Unique customer identifier | Unique, not null |
| customer_name | Customer name | Not null |
| city | Customer's city | Not null |

**Primary key:** `customer_id`

## 2. products.csv

| Column | Meaning | Expected Rule |
|---|---|---|
| product_id | Unique product identifier | Unique, not null |
| product_name | Product name | Not null |
| category | Product category | Not null |
| unit_price | Price per unit | Greater than 0 |

**Primary key:** `product_id`

## 3. orders.csv

| Column | Meaning | Expected Rule |
|---|---|---|
| order_id | Unique order identifier | Unique, not null |
| customer_id | Customer who placed the order | Must exist in customers.csv |
| order_date | Date of the order | Not null |
| product_id | Ordered product | Must exist in products.csv |
| quantity | Number of units ordered | Greater than 0 |

**Primary key:** `order_id`  
**Foreign keys:** `customer_id`, `product_id`

**Note:** Each row currently represents one product line per order. Multiple products per order will be supported in a future dataset revision.

## 4. payments.csv

| Column | Meaning | Expected Rule |
|---|---|---|
| payment_id | Unique payment identifier | Unique, not null |
| order_id | Related order identifier | Must exist in orders.csv |
| payment_method | Payment method | Not null |
| payment_status | Payment result/status | `paid`, `pending`, or `failed` |
| amount | Payment amount | Greater than 0 |

**Primary key:** `payment_id`  
**Foreign key:** `order_id`

## Current Validation Checks

The Python validation script checks:

1. Unique IDs across all four datasets.
2. Required fields are not null.
3. Order customer and product references exist.
4. Payment order references exist.
5. Quantity, product price, and payment amount are positive.
6. Payment status belongs to the allowed set.
7. Payment amount matches the related order line total.

## Data Limitations

- All records are synthetic and are not real customer transactions.
- The current dataset is intentionally small for learning and testing.
- Payment statuses are sample values, not verified payment-provider records.
- The current model treats each order row as a single product line.
- More advanced business rules and automated tests will be added later.



# RetailPulse — Data Dictionary

## Project Overview
RetailPulse is an e-commerce data engineering portfolio project.
All current records are synthetic data generated locally with Python.

Source directory: `data/raw/`
Validation script: `src/retailpulse/validate_data.py`

## 1. customers.csv

| Column | Meaning | Rule |
|---|---|---|
| customer_id | Customer identifier | Unique, not null |
| customer_name | Customer name | Not null |
| city | Customer city | Not null |

Primary key: `customer_id`

## 2. products.csv

| Column | Meaning | Rule |
|---|---|---|
| product_id | Product identifier | Unique, not null |
| product_name | Product name | Not null |
| category | Product category | Not null |
| unit_price | Price per unit | Greater than 0 |

Primary key: `product_id`

## 3. orders.csv

| Column | Meaning | Rule |
|---|---|---|
| order_id | Order identifier | Unique, not null |
| customer_id | Customer placing the order | Must exist in customers.csv |
| order_date | Order date | Not null |
| product_id | Ordered product | Must exist in products.csv |
| quantity | Units ordered | Greater than 0 |

Primary key: `order_id`
Foreign keys: `customer_id`, `product_id`

Each row currently represents one product line per order.

## 4. payments.csv

| Column | Meaning | Rule |
|---|---|---|
| payment_id | Payment identifier | Unique, not null |
| order_id | Related order | Must exist in orders.csv |
| payment_method | Payment method | Not null |
| payment_status | Payment status | paid, pending, or failed |
| amount | Payment amount | Greater than 0 |

Primary key: `payment_id`
Foreign key: `order_id`

## Validation Checks

1. Unique IDs
2. Required fields are not null
3. Order customer references exist
4. Order product references exist
5. Payment order references exist
6. Quantity, prices, and payment amounts are positive
7. Payment statuses are allowed
8. Payment amounts match order line totals

## Limitations

- All data is synthetic, not real customer data.
- The dataset is small and intended for learning.
- More advanced business rules and automated tests will be added later.
