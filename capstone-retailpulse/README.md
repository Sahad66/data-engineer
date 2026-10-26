
# RetailPulse — E-commerce Data Platform

## Overview

RetailPulse is an end-to-end data engineering portfolio project
designed to ingest, validate, transform, and model e-commerce
data for reliable business analytics.

## Planned Technology Stack

- Python
- PostgreSQL
- SQL
- dbt
- Apache Airflow
- Docker
- pytest
- GitHub Actions

## Planned Pipeline

Source Data → Ingestion → Validation → PostgreSQL
→ Data Warehouse Models → Automated Tests → Analytics

## Project Status

Phase 1: Foundation and source data setup.

## Data and Results

Dataset documentation, validation results, architecture,
and project outcomes will be added as the project develops.



## Local Setup

### Requirements
- Python 3.12 or another compatible Python version
- Git

### 1. Clone the repository

Clone the repository and navigate to the `capstone-retailpulse` directory.

### 2. Create and activate a virtual environment (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

For normal installation:

```powershell
python -m pip install -r requirements.txt
```

To install the exact versions captured in the lock file:

```powershell
python -m pip install -r requirements-lock.txt
```

### 4. Generate the synthetic source data

```powershell
python .\src\retailpulse\generate_data.py
```

### 5. Run data quality validation

```powershell
python .\src\retailpulse\validate_data.py
```

The validation script should report all checks as passed.

### Data Storage

Generated CSV files are stored in `data/raw/`.
Virtual environments, logs, and environment secrets should not be committed.

### Current Project Status

- Synthetic source data generation: completed
- Automated data quality validation: completed
- Data dictionary: completed
- PostgreSQL warehouse and ETL pipeline: planned next
