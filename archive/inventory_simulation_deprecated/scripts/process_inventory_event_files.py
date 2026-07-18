from pathlib import Path
from datetime import datetime
import shutil
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


INCOMING_DIR = Path("data/inventory_events/incoming")
PROCESSED_DIR = Path("data/inventory_events/processed")
FAILED_DIR = Path("data/inventory_events/failed")
LOG_DIR = Path("logs")

INCOMING_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
FAILED_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_COLUMNS = [
    "event_id",
    "event_timestamp",
    "product_id",
    "seller_id",
    "movement_type",
    "quantity_change",
    "reason",
    "source_system",
]

VALID_MOVEMENT_TYPES = {
    "RESTOCK",
    "ADJUSTMENT",
    "DAMAGED",
    "RETURN",
    "TRANSFER_IN",
    "TRANSFER_OUT",
}


def write_log(message: str) -> None:
    log_file = LOG_DIR / "inventory_event_pipeline.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def create_event_tables(engine) -> None:
    create_event_log_sql = """
    CREATE TABLE IF NOT EXISTS inventory_event_log (
        event_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        total_records INTEGER NOT NULL,
        valid_records INTEGER NOT NULL,
        failed_records INTEGER NOT NULL,
        status TEXT NOT NULL,
        error_message TEXT,
        processed_at TEXT NOT NULL
    );
    """

    create_event_records_sql = """
    CREATE TABLE IF NOT EXISTS inventory_event_records (
        event_id TEXT PRIMARY KEY,
        event_timestamp TEXT NOT NULL,
        product_id TEXT NOT NULL,
        seller_id TEXT NOT NULL,
        movement_type TEXT NOT NULL,
        quantity_change INTEGER NOT NULL,
        reason TEXT,
        source_system TEXT,
        file_name TEXT NOT NULL,
        processed_at TEXT NOT NULL
    );
    """

    create_failed_records_sql = """
    CREATE TABLE IF NOT EXISTS inventory_event_failed_records (
        failed_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        row_number INTEGER,
        event_id TEXT,
        product_id TEXT,
        seller_id TEXT,
        movement_type TEXT,
        quantity_change TEXT,
        failure_reason TEXT NOT NULL,
        failed_at TEXT NOT NULL
    );
    """

    with engine.begin() as connection:
        connection.execute(text(create_event_log_sql))
        connection.execute(text(create_event_records_sql))
        connection.execute(text(create_failed_records_sql))


def insert_event_log(
    engine,
    file_name: str,
    total_records: int,
    valid_records: int,
    failed_records: int,
    status: str,
    error_message: str = "",
) -> None:
    query = text(
        """
        INSERT INTO inventory_event_log (
            file_name,
            total_records,
            valid_records,
            failed_records,
            status,
            error_message,
            processed_at
        )
        VALUES (
            :file_name,
            :total_records,
            :valid_records,
            :failed_records,
            :status,
            :error_message,
            :processed_at
        )
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "file_name": file_name,
                "total_records": total_records,
                "valid_records": valid_records,
                "failed_records": failed_records,
                "status": status,
                "error_message": error_message,
                "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        )


def validate_file_schema(df: pd.DataFrame) -> list[str]:
    errors = []

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            errors.append(f"Missing required column: {column}")

    return errors


def validate_records(df: pd.DataFrame, engine) -> tuple[pd.DataFrame, pd.DataFrame]:
    policy_df = pd.read_sql(
        "SELECT product_id, seller_id FROM sim_inventory_policy",
        engine,
    )

    valid_product_seller_pairs = set(
        zip(policy_df["product_id"], policy_df["seller_id"])
    )

    valid_rows = []
    failed_rows = []

    for index, row in df.iterrows():
        failure_reasons = []

        event_id = str(row.get("event_id", "")).strip()
        product_id = str(row.get("product_id", "")).strip()
        seller_id = str(row.get("seller_id", "")).strip()
        movement_type = str(row.get("movement_type", "")).strip().upper()
        quantity_change = row.get("quantity_change", None)

        if not event_id:
            failure_reasons.append("event_id is missing")

        if not product_id:
            failure_reasons.append("product_id is missing")

        if not seller_id:
            failure_reasons.append("seller_id is missing")

        if movement_type not in VALID_MOVEMENT_TYPES:
            failure_reasons.append("invalid movement_type")

        try:
            quantity_change_int = int(quantity_change)
            if quantity_change_int == 0:
                failure_reasons.append("quantity_change cannot be zero")
        except Exception:
            quantity_change_int = None
            failure_reasons.append("quantity_change is not a valid integer")

        if product_id and seller_id:
            if (product_id, seller_id) not in valid_product_seller_pairs:
                failure_reasons.append("product_id and seller_id pair not found in inventory policy")

        if failure_reasons:
            failed_rows.append(
                {
                    "file_name": row.get("file_name", ""),
                    "row_number": index + 2,
                    "event_id": event_id,
                    "product_id": product_id,
                    "seller_id": seller_id,
                    "movement_type": movement_type,
                    "quantity_change": str(quantity_change),
                    "failure_reason": "; ".join(failure_reasons),
                    "failed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        else:
            valid_rows.append(
                {
                    "event_id": event_id,
                    "event_timestamp": row["event_timestamp"],
                    "product_id": product_id,
                    "seller_id": seller_id,
                    "movement_type": movement_type,
                    "quantity_change": quantity_change_int,
                    "reason": row.get("reason", ""),
                    "source_system": row.get("source_system", ""),
                    "file_name": row.get("file_name", ""),
                    "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

    return pd.DataFrame(valid_rows), pd.DataFrame(failed_rows)


def append_dataframe_to_table(df: pd.DataFrame, table_name: str, engine) -> None:
    if not df.empty:
        df.to_sql(table_name, engine, if_exists="append", index=False)


def process_file(file_path: Path, engine) -> None:
    file_name = file_path.name
    write_log(f"STARTED | Processing file {file_name}")

    try:
        df = pd.read_csv(file_path)
        df["file_name"] = file_name

        schema_errors = validate_file_schema(df)

        if schema_errors:
            error_message = "; ".join(schema_errors)
            insert_event_log(
                engine,
                file_name=file_name,
                total_records=len(df),
                valid_records=0,
                failed_records=len(df),
                status="FAILED",
                error_message=error_message,
            )

            failed_target = FAILED_DIR / file_name
            shutil.move(str(file_path), str(failed_target))

            write_log(f"FAILED | {file_name} | {error_message}")
            print(f"FAILED | {file_name} | {error_message}")
            return

        valid_df, failed_df = validate_records(df, engine)

        append_dataframe_to_table(valid_df, "inventory_event_records", engine)
        append_dataframe_to_table(failed_df, "inventory_event_failed_records", engine)

        status = "SUCCESS" if failed_df.empty else "PARTIAL_SUCCESS"

        insert_event_log(
            engine,
            file_name=file_name,
            total_records=len(df),
            valid_records=len(valid_df),
            failed_records=len(failed_df),
            status=status,
        )

        processed_target = PROCESSED_DIR / file_name
        shutil.move(str(file_path), str(processed_target))

        write_log(
            f"{status} | {file_name} | total={len(df)} | valid={len(valid_df)} | failed={len(failed_df)}"
        )

        print(
            f"{status} | {file_name} | total={len(df)} | valid={len(valid_df)} | failed={len(failed_df)}"
        )

    except Exception as error:
        error_message = str(error)

        insert_event_log(
            engine,
            file_name=file_name,
            total_records=0,
            valid_records=0,
            failed_records=0,
            status="FAILED",
            error_message=error_message,
        )

        failed_target = FAILED_DIR / file_name
        shutil.move(str(file_path), str(failed_target))

        write_log(f"FAILED | {file_name} | {error_message}")
        print(f"FAILED | {file_name} | {error_message}")


def main() -> None:
    print("Starting inventory event pipeline...")

    engine = get_engine()
    create_event_tables(engine)

    incoming_files = sorted(INCOMING_DIR.glob("*.csv"))

    if not incoming_files:
        print("No incoming inventory event files found.")
        write_log("NO_FILES | No incoming inventory event files found")
        return

    for file_path in incoming_files:
        process_file(file_path, engine)

    print("Inventory event pipeline completed.")


if __name__ == "__main__":
    main()