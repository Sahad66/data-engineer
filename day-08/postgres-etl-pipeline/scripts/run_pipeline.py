
import logging
import os
import subprocess
import sys
from pathlib import Path

import psycopg

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)


def run_step(script_name):
    script = SCRIPTS_DIR / script_name
    logger.info("Starting step: %s", script_name)

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=BASE_DIR,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_name} failed with exit code {result.returncode}"
        )

    logger.info("Completed step: %s", script_name)


def main():
    try:
        # Extract/validate the source, then generate clean/rejected CSVs.
        run_step("extract_orders.py")
        run_step("transform_orders.py")

        # Run the PostgreSQL load and audit integration.
        run_step("audit_pipeline.py")

        logger.info("End-to-end pipeline completed successfully")
        print("END-TO-END PIPELINE: SUCCESS")

    except Exception:
        logger.exception("End-to-end pipeline failed")
        print("END-TO-END PIPELINE: FAILURE", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
