
import subprocess
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent

steps = [
    ("Validate raw data", "validate_orders.py"),
    ("Clean data", "run_cleaning.py"),
    ("Audit clean data", "audit_clean_data.py"),
    ("Test clean data", "test_clean_data.py"),
]

print("FULL PIPELINE STARTED")

for step_name, script_name in steps:
    script_path = project_dir / "scripts" / script_name

    print(f"\nSTEP: {step_name}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=project_dir,
    )

    if result.returncode != 0:
        print(f"PIPELINE FAILED at: {step_name}")
        sys.exit(1)

print("\nPIPELINE STATUS: SUCCESS")
