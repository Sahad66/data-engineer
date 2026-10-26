
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_incremental_pipeline_script_exists():
    """Python incremental pipeline script থাকা উচিত."""
    script = (
        PROJECT_ROOT
        / "src"
        / "retailpulse"
        / "run_incremental_pipeline.py"
    )
    assert script.is_file()


def test_incremental_sql_files_exist():
    """Incremental loading-এর গুরুত্বপূর্ণ SQL files থাকা উচিত."""
    sql_files = [
        "01_incremental_demo.sql",
        "02_first_incremental_load.sql",
        "03_create_audit_log.sql",
        "06_validate_incremental_data.sql",
        "07_incremental_quality_report.sql",
    ]

    sql_dir = PROJECT_ROOT / "sql" / "incremental"

    for filename in sql_files:
        assert (sql_dir / filename).is_file(), (
            f"Missing SQL file: {filename}"
        )


def test_environment_example_exists():
    """Example configuration file থাকা উচিত."""
    env_example = PROJECT_ROOT / ".env.example"
    assert env_example.is_file()


def test_env_example_does_not_contain_real_password():
    """Example file-এ password value খালি থাকা উচিত."""
    env_example = PROJECT_ROOT / ".env.example"
    content = env_example.read_text(encoding="utf-8")

    password_lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip().startswith("RETAILPULSE_DB_PASSWORD=")
    ]

    assert password_lines, "Password variable is missing"
    assert password_lines[0] == "RETAILPULSE_DB_PASSWORD=", (
        "Do not store a real password in .env.example"
    )


def test_gitignore_excludes_env_file():
    """Git যেন local .env file ignore করে."""
    gitignore = PROJECT_ROOT / ".gitignore"
    assert gitignore.is_file()

    lines = gitignore.read_text(encoding="utf-8").splitlines()
    assert ".env" in [line.strip() for line in lines]
