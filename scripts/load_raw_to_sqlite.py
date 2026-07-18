from pathlib import Path
from datetime import datetime
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


RAW_DATA_DIR = Path("data/raw")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

RAW_TABLE_MAPPING = {
    "olist_customers_dataset.csv": "raw_customers",
    "olist_geolocation_dataset.csv": "raw_geolocation",
    "olist_order_items_dataset.csv": "raw_order_items",
    "olist_order_payments_dataset.csv": "raw_order_payments",
    "olist_order_reviews_dataset.csv": "raw_order_reviews",
    "olist_orders_dataset.csv": "raw_orders",
    "olist_products_dataset.csv": "raw_products",
    "olist_sellers_dataset.csv": "raw_sellers",
    "product_category_name_translation.csv": "raw_product_category_translation",
}


def write_log(message: str) -> None:
    log_file = LOG_DIR / "raw_load.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def create_raw_load_audit_table(engine) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS raw_load_audit (
        audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        table_name TEXT NOT NULL,
        row_count INTEGER,
        load_status TEXT NOT NULL,
        error_message TEXT,
        loaded_at TEXT NOT NULL
    );
    """

    with engine.begin() as connection:
        connection.execute(text(query))


def insert_audit_record(
    engine,
    file_name: str,
    table_name: str,
    row_count: int,
    load_status: str,
    error_message: str = "",
) -> None:
    query = text(
        """
        INSERT INTO raw_load_audit (
            file_name,
            table_name,
            row_count,
            load_status,
            error_message,
            loaded_at
        )
        VALUES (
            :file_name,
            :table_name,
            :row_count,
            :load_status,
            :error_message,
            :loaded_at
        );
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "file_name": file_name,
                "table_name": table_name,
                "row_count": row_count,
                "load_status": load_status,
                "error_message": error_message,
                "loaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        )


def load_csv_to_raw_table(engine, file_name: str, table_name: str) -> None:
    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        error_message = f"File not found: {file_path}"
        write_log(f"FAILED | {file_name} | {error_message}")
        insert_audit_record(engine, file_name, table_name, 0, "FAILED", error_message)
        return

    try:
        df = pd.read_csv(file_path)

        # Add metadata columns commonly used in raw data layers
        df["_source_file"] = file_name
        df["_loaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        df.to_sql(table_name, engine, if_exists="replace", index=False)

        row_count = len(df)

        write_log(f"SUCCESS | {file_name} loaded into {table_name} | rows={row_count}")
        insert_audit_record(engine, file_name, table_name, row_count, "SUCCESS")

        print(f"Loaded {file_name} into {table_name} | rows: {row_count}")

    except Exception as error:
        error_message = str(error)
        write_log(f"FAILED | {file_name} | {error_message}")
        insert_audit_record(engine, file_name, table_name, 0, "FAILED", error_message)
        print(f"Failed to load {file_name}: {error_message}")


def main() -> None:
    print("Starting raw data load into SQLite database...\n")

    engine = get_engine()
    create_raw_load_audit_table(engine)

    for file_name, table_name in RAW_TABLE_MAPPING.items():
        load_csv_to_raw_table(engine, file_name, table_name)

    print("\nRaw data load completed.")
    print("Database created: retail_intelligence.db")
    print("Audit table created: raw_load_audit")
    print("Log file created: logs/raw_load.log")


if __name__ == "__main__":
    main()