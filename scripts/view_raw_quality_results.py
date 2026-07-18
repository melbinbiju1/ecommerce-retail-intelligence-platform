from pathlib import Path
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


def main() -> None:
    engine = get_engine()

    query = text(
        """
        SELECT
            check_name,
            table_name,
            failed_count,
            status,
            severity,
            checked_at
        FROM raw_data_quality_results
        ORDER BY
            CASE severity
                WHEN 'critical' THEN 1
                WHEN 'warning' THEN 2
                ELSE 3
            END,
            status,
            check_name
        """
    )

    with engine.begin() as connection:
        results_df = pd.read_sql(query, connection)

    print(results_df)

    failed_df = results_df[results_df["status"] == "FAILED"]

    print("\nFailed checks:")
    if failed_df.empty:
        print("No failed checks.")
    else:
        print(failed_df[["check_name", "table_name", "failed_count", "severity"]])


if __name__ == "__main__":
    main()