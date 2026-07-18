from pathlib import Path
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


TABLES = [
    "ops_event_log",
    "ops_event_records",
    "ops_event_failed_records",
]


def main() -> None:
    engine = get_engine()

    print("Operational event pipeline verification\n")

    results = []

    for table_name in TABLES:
        with engine.begin() as connection:
            exists_query = text(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = :table_name
                """
            )

            exists_result = pd.read_sql(
                exists_query,
                connection,
                params={"table_name": table_name},
            )

            exists = not exists_result.empty
            row_count = None

            if exists:
                row_count_query = text(f"SELECT COUNT(*) AS row_count FROM {table_name}")
                row_count = int(
                    pd.read_sql(row_count_query, connection)["row_count"].iloc[0]
                )

            results.append(
                {
                    "table_name": table_name,
                    "exists": exists,
                    "row_count": row_count,
                }
            )

    results_df = pd.DataFrame(results)
    print(results_df)

    print("\nLatest event log records:")

    latest_log_df = pd.read_sql(
        """
        SELECT *
        FROM ops_event_log
        ORDER BY processed_at DESC
        LIMIT 5
        """,
        engine,
    )

    print(latest_log_df)

    output_path = Path("data/processed/operational_event_pipeline_verification_report.csv")
    results_df.to_csv(output_path, index=False)

    print(f"\nVerification report saved to: {output_path}")


if __name__ == "__main__":
    main()