
from datetime import datetime
from pathlib import Path
import subprocess
import sys

project_dir = Path(__file__).resolve().parent.parent
log_dir = project_dir / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

report_file = log_dir / "pipeline_report.txt"

steps = [
    ("Raw validation", "validate_orders.py"),
    ("Cleaning", "run_cleaning.py"),
    ("Data audit", "audit_clean_data.py"),
    ("Clean data test", "test_clean_data.py"),
]

results = []
pipeline_success = True

for step_name, script_name in steps:
    script_path = project_dir / "scripts" / script_name

    print(f"\nRunning: {step_name}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )

    passed = result.returncode == 0
    status = "PASS" if passed else "FAIL"

    results.append(f"{step_name}: {status}")
    print(f"{step_name}: {status}")

    if result.stdout:
        print(result.stdout)

    if not passed:
        if result.stderr:
            print(result.stderr)

        pipeline_success = False
        results.append("Pipeline stopped after failure.")
        break

final_status = (
    "SUCCESS" if pipeline_success else "FAILED"
)

report = [
    "PIPELINE EXECUTION REPORT",
    f"Run time: {datetime.now().isoformat(timespec='seconds')}",
    *results,
    f"FINAL STATUS: {final_status}",
]

report_file.write_text(
    "\n".join(report) + "\n",
    encoding="utf-8",
)

print("\n" + "=" * 30)
print(f"FINAL STATUS: {final_status}")
print(f"Report saved: {report_file}")

if not pipeline_success:
    sys.exit(1)

