import os
from pathlib import Path

import pandas as pd
import pytest
from sqlalchemy import text

from src.cloud.azure_sql_database import get_azure_sql_engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = PROJECT_ROOT / "data" / "processed" / "azure_sql_connection_test_report.csv"


@pytest.mark.skipif(
    os.getenv("RUN_AZURE_SQL_TESTS", "false").lower() != "true",
    reason="Azure SQL live test skipped. Set RUN_AZURE_SQL_TESTS=true to enable.",
)
def test_azure_sql_connection() -> None:
    """
    Tests Azure SQL Database connectivity.

    This is a live cloud test and is skipped during normal pytest runs to avoid
    failures when Azure SQL is paused, unavailable, or intentionally disabled
    for cost control.
    """
    engine = get_azure_sql_engine()

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1 AS connection_test"))
        row = result.fetchone()

    assert row is not None
    assert row[0] == 1

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    report_df = pd.DataFrame(
        [
            {
                "test_name": "azure_sql_connection",
                "status": "passed",
                "connection_test": row[0],
            }
        ]
    )

    report_df.to_csv(REPORT_PATH, index=False)


if __name__ == "__main__":
    os.environ["RUN_AZURE_SQL_TESTS"] = "true"
    test_azure_sql_connection()