# E-commerce Sales Data Warehouse

## Project Overview
A PostgreSQL-based E-commerce Sales Data Warehouse that transforms raw order data into structured sales facts and dimensions.

## Tech Stack
- PostgreSQL
- SQL
- Common Table Expressions (CTEs)
- Window Functions
- Data Quality Validation
- Git and GitHub

## Data Flow
Raw Orders → Data Cleaning and Transformation → Dimension Tables → Fact Sales → Business KPI Reports

## Warehouse Tables
- `ecommerce_dw.raw_orders`
- `ecommerce_dw.dim_product`
- `ecommerce_dw.dim_customer`
- `ecommerce_dw.dim_date`
- `ecommerce_dw.fact_sales`

## Business Reports
- Total orders and units sold
- Total revenue and average order value
- Category-wise sales
- Top-selling products
- Monthly revenue trend
- Customer-wise spending

## Data Quality Checks
- Duplicate business keys
- Invalid quantities and negative amounts
- Missing dimension relationships
- Revenue reconciliation
- Raw-to-warehouse row-count comparison

## How to Run
Run the SQL scripts in order using PostgreSQL:

1. `part17_warehouse.sql`
2. `part18_transform.sql`
3. `part19_sales_reports.sql`
4. `part20_final_validation.sql`

Example:

```powershell
psql -U postgres -d day9_advanced_sql -f ".\sql\part17_warehouse.sql"
```

## Learning Outcomes
- Designed a star-schema-style warehouse
- Practiced SQL-based ETL
- Used primary keys, foreign keys, constraints, CTEs and window functions
- Built business KPI queries
- Performed data quality and reconciliation checks

## Notes
The sample dataset is for learning and demonstration. Production pipelines need controlled source batches, reliable incremental loading, logging, and automated testing.
