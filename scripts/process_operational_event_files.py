from pathlib import Path
from datetime import datetime
import shutil
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


INCOMING_DIR = Path("data/operational_events/incoming")
PROCESSED_DIR = Path("data/operational_events/processed")
FAILED_DIR = Path("data/operational_events/failed")
LOG_DIR = Path("logs")

INCOMING_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
FAILED_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_COLUMNS = [
    "event_id",
    "event_timestamp",
    "event_type",
    "severity",
    "business_area",
    "entity_id",
    "entity_name",
    "metric_name",
    "actual_value",
    "expected_value",
    "event_description",
    "recommended_action",
    "source_system",
]

VALID_EVENT_TYPES = {
    "LATE_DELIVERY",
    "PAYMENT_FAILURE",
    "LOW_REVIEW",
    "ORDER_CANCELLED",
    "HIGH_FREIGHT_COST",
    "SELLER_DELAY_RISK",
    "REVENUE_DROP",
    "CATEGORY_DEMAND_DROP",
}

VALID_SEVERITIES = {"low", "medium", "high", "critical"}


def write_log(message: str) -> None:
    log_file = LOG_DIR / "operational_event_pipeline.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def create_event_tables(engine) -> None:
    create_event_log_sql = """
    CREATE TABLE IF NOT EXISTS ops_event_log (
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
    CREATE TABLE IF NOT EXISTS ops_event_records (
        event_id TEXT PRIMARY KEY,
        event_timestamp TEXT NOT NULL,
        event_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        business_area TEXT NOT NULL,
        entity_id TEXT,
        entity_name TEXT,
        metric_name TEXT NOT NULL,
        actual_value REAL,
        expected_value REAL,
        event_description TEXT NOT NULL,
        recommended_action TEXT NOT NULL,
        source_system TEXT,
        file_name TEXT NOT NULL,
        processed_at TEXT NOT NULL
    );
    """

    create_failed_records_sql = """
    CREATE TABLE IF NOT EXISTS ops_event_failed_records (
        failed_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        row_number INTEGER,
        event_id TEXT,
        event_type TEXT,
        severity TEXT,
        business_area TEXT,
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
        INSERT INTO ops_event_log (
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


def validate_records(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_rows = []
    failed_rows = []

    for index, row in df.iterrows():
        failure_reasons = []

        event_id = str(row.get("event_id", "")).strip()
        event_type = str(row.get("event_type", "")).strip().upper()
        severity = str(row.get("severity", "")).strip().lower()
        business_area = str(row.get("business_area", "")).strip()
        metric_name = str(row.get("metric_name", "")).strip()
        event_description = str(row.get("event_description", "")).strip()
        recommended_action = str(row.get("recommended_action", "")).strip()

        if not event_id:
            failure_reasons.append("event_id is missing")

        if event_type not in VALID_EVENT_TYPES:
            failure_reasons.append("invalid event_type")

        if severity not in VALID_SEVERITIES:
            failure_reasons.append("invalid severity")

        if not business_area:
            failure_reasons.append("business_area is missing")

        if not metric_name:
            failure_reasons.append("metric_name is missing")

        if not event_description:
            failure_reasons.append("event_description is missing")

        if not recommended_action:
            failure_reasons.append("recommended_action is missing")

        if failure_reasons:
            failed_rows.append(
                {
                    "file_name": row.get("file_name", ""),
                    "row_number": index + 2,
                    "event_id": event_id,
                    "event_type": event_type,
                    "severity": severity,
                    "business_area": business_area,
                    "failure_reason": "; ".join(failure_reasons),
                    "failed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        else:
            valid_rows.append(
                {
                    "event_id": event_id,
                    "event_timestamp": row["event_timestamp"],
                    "event_type": event_type,
                    "severity": severity,
                    "business_area": business_area,
                    "entity_id": row.get("entity_id", ""),
                    "entity_name": row.get("entity_name", ""),
                    "metric_name": metric_name,
                    "actual_value": row.get("actual_value", None),
                    "expected_value": row.get("expected_value", None),
                    "event_description": event_description,
                    "recommended_action": recommended_action,
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

            shutil.move(str(file_path), str(FAILED_DIR / file_name))

            write_log(f"FAILED | {file_name} | {error_message}")
            print(f"FAILED | {file_name} | {error_message}")
            return

        valid_df, failed_df = validate_records(df)

        append_dataframe_to_table(valid_df, "ops_event_records", engine)
        append_dataframe_to_table(failed_df, "ops_event_failed_records", engine)

        status = "SUCCESS" if failed_df.empty else "PARTIAL_SUCCESS"

        insert_event_log(
            engine,
            file_name=file_name,
            total_records=len(df),
            valid_records=len(valid_df),
            failed_records=len(failed_df),
            status=status,
        )

        shutil.move(str(file_path), str(PROCESSED_DIR / file_name))

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

        shutil.move(str(file_path), str(FAILED_DIR / file_name))

        write_log(f"FAILED | {file_name} | {error_message}")
        print(f"FAILED | {file_name} | {error_message}")


def main() -> None:
    print("Starting operational event pipeline...")

    engine = get_engine()
    create_event_tables(engine)

    incoming_files = sorted(INCOMING_DIR.glob("*.csv"))

    if not incoming_files:
        print("No incoming operational event files found.")
        write_log("NO_FILES | No incoming operational event files found")
        return

    for file_path in incoming_files:
        process_file(file_path, engine)

    print("Operational event pipeline completed.")


if __name__ == "__main__":
    main()