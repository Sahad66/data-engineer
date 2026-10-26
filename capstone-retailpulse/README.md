# RetailPulse - E-commerce Data Engineering Platform

## Overview

RetailPulse is an end-to-end data engineering portfolio project built to demonstrate reliable e-commerce data ingestion, validation, PostgreSQL-based data processing, incremental loading, data quality checks, audit logging, and pipeline recovery.

The project uses synthetic e-commerce data to demonstrate practical data engineering workflows.

## Technology Stack

- Python
- PostgreSQL
- SQL
- pytest
- PowerShell
- Git and GitHub


Additional technologies such as dbt, Apache Airflow, Docker, and GitHub Actions may be considered for future extensions if they are not yet implemented.

## Pipeline Architecture

```text
Synthetic E-commerce Data
          |
          v
     Data Ingestion
          |
          v
   Data Validation
          |
          v
 PostgreSQL Source/Target
          |
          v
 Incremental Load + Watermark
          |
          v
 Data Quality Validation
          |
          v
 Audit Logging and Monitoring
          |
          v
 Tests, Recovery, and Automation
```

## Implemented Capabilities

- Synthetic e-commerce source data generation
- Data validation and quality checks
- PostgreSQL integration
- Incremental data loading
- Watermark/checkpoint tracking
- Duplicate prevention and upsert handling
- Audit run tracking
- Failure simulation and recovery verification
- SQL monitoring queries and operational runbook
- PowerShell pipeline runner
- Windows Task Scheduler setup and manual execution test
- Automated tests using pytest
- Git ignore rules for local secrets and generated files

## Testing

Run the automated test suite from the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The latest reported test result:

```text
5 passed
```

Run the tests again after making changes to confirm the current result.

## Local Setup

### Requirements

- Python
- PostgreSQL
- Git
- Windows PowerShell (for the provided Windows automation scripts)

### 1. Clone the repository

```powershell
git clone https://github.com/Sahad66/data-engineer.git
cd data-engineer\capstone-retailpulse
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements-lock.txt
```

If you need the exact versions recorded in the lock file:

```powershell
python -m pip install -r requirements-lock.txt
```

### 4. Configure local environment

Review `.env.example` and create a local `.env` file if the project scripts require environment variables. Keep credentials and passwords out of Git.

### 5. Generate synthetic source data

```powershell
python .\src\retailpulse\generate_data.py
```

### 6. Run data validation

```powershell
python .\src\retailpulse\validate_data.py
```

Follow the validation output to confirm whether the checks pass.

### 7. Run automated tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Refer to the pipeline scripts and SQL files for the exact PostgreSQL setup and incremental execution commands.

## Security

- Local `.env` files should not be committed.
- PostgreSQL credentials should be stored outside source code.
- Use `.env.example` to document required variable names without real secrets.
- Review `git status` before committing changes.

## Current Status

The project includes incremental pipeline functionality, audit tracking, data quality validation, recovery testing, operational SQL, Windows automation, and automated tests.

The latest test run completed successfully with **5 passed**.

## Future Improvements

Potential extensions include:

- dbt-based warehouse transformations
- Apache Airflow orchestration
- Docker-based environment setup
- GitHub Actions continuous integration
- Business KPI dashboard
- Additional integration and data reconciliation tests

## Repository

GitHub: https://github.com/Sahad66/data-engineer.git


