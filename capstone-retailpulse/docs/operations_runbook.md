
# RetailPulse Incremental Pipeline — Operations Runbook

## 1. Purpose
This document explains how to run and monitor the
RetailPulse incremental pipeline.

## 2. Run the pipeline
From the capstone-retailpulse project root:

```powershell
python src\retailpulse\run_incremental_pipeline.py
```

## 3. Review the logs
Check the logs directory for the incremental pipeline log.
Review recent entries for successful runs and errors.

## 4. Monitor pipeline runs
Run the monitoring SQL:

```powershell
psql -U postgres -d retailpulse -v ON_ERROR_STOP=1 -f sql/incremental/08_monitor_incremental_runs.sql
```

## 5. Validate data quality
Run the quality report:

```powershell
psql -U postgres -d retailpulse -v ON_ERROR_STOP=1 -f sql/incremental/07_incremental_quality_report.sql
```

Expected result: all five quality checks PASS.

## 6. If a run fails
1. Read the Python error output.
2. Inspect the pipeline log, if available.
3. Review the latest FAILED audit record.
4. Identify and fix the root cause.
5. Rerun the pipeline without failure simulation.
6. Confirm a new SUCCESS record.
7. Re-run data quality checks.

## 7. Safety
- Never commit passwords or secrets.
- Do not delete audit history just to hide failures.
- Validate target data after recovery.
- Review SQL changes before running them.
