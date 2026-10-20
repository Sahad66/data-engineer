
import logging
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SQL_FILE = PROJECT_DIR / "sql" / "clean_orders.sql"
LOG_DIR = PROJECT_DIR / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def run_cleaning():
    logging.info("Data cleaning pipeline started.")

    try:
        if not SQL_FILE.exists():
            raise FileNotFoundError(f"SQL file not found: {SQL_FILE}")

        subprocess.run(
            [
                "psql",
                "-U", "postgres",
                "-d", "day-2",
                "-v", "ON_ERROR_STOP=1",
                "-f", str(SQL_FILE),
            ],
            check=True,
        )

        logging.info("Data cleaning completed successfully.")
        print("Data cleaning completed successfully!")

    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        logging.exception("Data cleaning pipeline failed.")
        print(f"Pipeline failed: {error}")
        raise

if __name__ == "__main__":
    run_cleaning()
