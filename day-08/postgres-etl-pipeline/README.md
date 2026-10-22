
# Day 8 — PostgreSQL ETL Pipeline

## Project Overview
A Python ETL pipeline that extracts ecommerce orders from CSV,
validates and transforms records, loads clean data into PostgreSQL,
and records pipeline execution results in an audit table.

## Architecture
CSV Source
-> Extract
-> Validate and Transform
-> Clean / Rejected CSV
-> PostgreSQL Load
-> Audit and Verification

## Technologies
- Python
- PostgreSQL
- psycopg
- CSV
- SQL
- Git and GitHub

## Data Quality Rules
- order_id must be an integer and unique in the target table.
- customer_id must not be empty.
- quantity must be greater than zero.
- unit_price must be zero or greater.
- Invalid rows are stored with a rejection reason.

## Project Structure
- data/: source, clean and rejected CSV files
- scripts/: extraction, transformation, loading and verification
- logs/: pipeline logs
- sql/: SQL scripts

## How to Run
1. Install psycopg:
   python -m pip install "psycopg[binary]"

2. Create the PostgreSQL database and tables.

3. Ensure the PostgreSQL connection settings are correct.

4. Run the pipeline:
   python scripts/run_pipeline.py

5. Verify the results:
   python scripts/verify_pipeline.py

## Data Reconciliation
Input rows = Clean rows + Rejected rows

## Notes
- Do not commit passwords or other secrets.
- Confirm that the PostgreSQL database and audit table exist
  before running the pipeline.
