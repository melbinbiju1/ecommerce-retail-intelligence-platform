from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cloud.azure_sql_database import get_azure_sql_engine  # noqa: E402


OUTPUT_REPORT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "azure_sql_setup_verification_report.csv"
)


EXPECTED_LOCAL_FILES = [
    "src/cloud/azure_sql_database.py",
    "scripts/test_azure_sql_connection.py",
    "scripts/migrate_curated_data_to_azure_sql.py",
    "scripts/verify_azure_sql_setup.py",
    ".env.example",
    "requirements.txt",
]

EXPECTED_ENV_EXAMPLE_CONTENT = [
    "AZURE_SQL_SERVER",
    "AZURE_SQL_DATABASE",
    "AZURE_SQL_USERNAME",
    "AZURE_SQL_PASSWORD",
    "AZURE_SQL_DRIVER",
]

EXPECTED_REQUIREMENTS_CONTENT = [
    "sqlalchemy",
    "pyodbc",
    "python-dotenv",
]

EXPECTED_AZURE_SQL_TABLES = [
    "dim_date",
    "dim_customer",
    "dim_product",
    "dim_seller",
    "fact_sales",
    "fact_delivery",
    "fact_payments",
    "fact_reviews",
    "ops_daily_metrics",
    "ops_seller_metrics",
    "ops_category_metrics",
    "ops_anomaly_rules",
    "ops_anomaly_alerts",
    "ops_event_log",
    "ops_event_records",
]


def read_file_safely(relative_path: str) -> str:
    file_path = PROJECT_ROOT / relative_path

    if not file_path.exists():
        return ""

    encodings = ["utf-8", "utf-8-sig", "utf-16", "cp1252"]

    for encoding in encodings:
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    return file_path.read_text(errors="ignore")


def file_contains(relative_path: str, text_value: str) -> bool:
    return text_value in read_file_safely(relative_path)


def get_table_row_count(table_name: str) -> int:
    engine = get_azure_sql_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text(f"SELECT COUNT(*) FROM dbo.{table_name}")
        )
        return int(result.scalar())


def azure_table_exists(table_name: str) -> bool:
    engine = get_azure_sql_engine()

    query = text(
        """
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'dbo'
          AND TABLE_NAME = :table_name
        """
    )

    with engine.connect() as connection:
        result = connection.execute(query, {"table_name": table_name})
        return int(result.scalar()) > 0


def main() -> None:
    results = []

    for relative_path in EXPECTED_LOCAL_FILES:
        file_path = PROJECT_ROOT / relative_path
        results.append(
            {
                "check_type": "local_file_exists",
                "item": relative_path,
                "passed": file_path.exists(),
                "row_count": None,
            }
        )

    for text_value in EXPECTED_ENV_EXAMPLE_CONTENT:
        results.append(
            {
                "check_type": "env_example_content",
                "item": text_value,
                "passed": file_contains(".env.example", text_value),
                "row_count": None,
            }
        )

    for text_value in EXPECTED_REQUIREMENTS_CONTENT:
        results.append(
            {
                "check_type": "requirements_content",
                "item": text_value,
                "passed": file_contains("requirements.txt", text_value),
                "row_count": None,
            }
        )

    for table_name in EXPECTED_AZURE_SQL_TABLES:
        exists = azure_table_exists(table_name)

        row_count = get_table_row_count(table_name) if exists else 0

        results.append(
            {
                "check_type": "azure_sql_table_loaded",
                "item": table_name,
                "passed": exists and row_count > 0,
                "row_count": row_count,
            }
        )

    results_df = pd.DataFrame(results)

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_REPORT, index=False)

    print(results_df)

    failed_checks = results_df[results_df["passed"] == False]

    print(f"\nVerification report saved to: {OUTPUT_REPORT}")

    if failed_checks.empty:
        print("\nAzure SQL setup verification passed.")
    else:
        print("\nSome Azure SQL setup checks failed:")
        print(failed_checks[["check_type", "item", "row_count"]])
        raise RuntimeError("Azure SQL setup verification failed.")


if __name__ == "__main__":
    main()