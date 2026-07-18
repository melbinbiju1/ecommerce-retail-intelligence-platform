from pathlib import Path
from datetime import datetime
import sys
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


SQL_FILE_PATH = Path("sql/kpi_views/create_kpi_views.sql")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def write_log(message: str) -> None:
    log_file = LOG_DIR / "kpi_views.log"
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
    print("Creating KPI views...")

    if not SQL_FILE_PATH.exists():
        raise FileNotFoundError(f"SQL file not found: {SQL_FILE_PATH}")

    sql_script = SQL_FILE_PATH.read_text(encoding="utf-8")
    sql_statements = split_sql_statements(sql_script)

    engine = get_engine()

    try:
        with engine.begin() as connection:
            for statement in sql_statements:
                connection.execute(text(statement))

        write_log("SUCCESS | KPI views created successfully")
        print("KPI views created successfully.")
        print("Log file created: logs/kpi_views.log")

    except Exception as error:
        write_log(f"FAILED | KPI view creation failed | {error}")
        print(f"KPI view creation failed: {error}")
        raise


if __name__ == "__main__":
    main()