from pathlib import Path
from datetime import datetime
import sys
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


SQL_FILE_PATH = Path("sql/staging/create_staging_tables.sql")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def write_log(message: str) -> None:
    log_file = LOG_DIR / "staging_load.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def split_sql_statements(sql_script: str) -> list[str]:
    return [
        statement.strip()
        for statement in sql_script.split(";")
        if statement.strip()
    ]


def main() -> None:
    print("Creating staging tables...")

    if not SQL_FILE_PATH.exists():
        raise FileNotFoundError(f"SQL file not found: {SQL_FILE_PATH}")

    sql_script = SQL_FILE_PATH.read_text(encoding="utf-8")
    sql_statements = split_sql_statements(sql_script)

    engine = get_engine()

    try:
        with engine.begin() as connection:
            for statement in sql_statements:
                connection.execute(text(statement))

        write_log("SUCCESS | Staging tables created successfully")
        print("Staging tables created successfully.")
        print("Log file created: logs/staging_load.log")

    except Exception as error:
        write_log(f"FAILED | Staging table creation failed | {error}")
        print(f"Staging table creation failed: {error}")
        raise


if __name__ == "__main__":
    main()