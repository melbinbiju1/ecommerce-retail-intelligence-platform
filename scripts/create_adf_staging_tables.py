from pathlib import Path
import sys

from sqlalchemy import text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cloud.azure_sql_database import get_azure_sql_engine  # noqa: E402


SQL_FILE = PROJECT_ROOT / "sql" / "azure_sql" / "create_adf_staging_tables.sql"


def split_sql_batches(sql_text: str) -> list[str]:
    batches = []
    current_batch = []

    for line in sql_text.splitlines():
        if line.strip().upper() == "GO":
            batch = "\n".join(current_batch).strip()
            if batch:
                batches.append(batch)
            current_batch = []
        else:
            current_batch.append(line)

    final_batch = "\n".join(current_batch).strip()
    if final_batch:
        batches.append(final_batch)

    return batches


def main() -> None:
    if not SQL_FILE.exists():
        raise FileNotFoundError(f"SQL file not found: {SQL_FILE}")

    sql_text = SQL_FILE.read_text(encoding="utf-8")
    batches = split_sql_batches(sql_text)

    engine = get_azure_sql_engine()

    with engine.begin() as connection:
        for batch in batches:
            connection.execute(text(batch))

    print("ADF staging table created successfully.")
    print("Created table: dbo.adf_stg_orders_raw")


if __name__ == "__main__":
    main()