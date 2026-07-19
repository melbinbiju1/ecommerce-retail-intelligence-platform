from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cloud.azure_sql_database import test_azure_sql_connection  # noqa: E402


OUTPUT_REPORT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "azure_sql_connection_test_report.csv"
)


def main() -> None:
    print("Testing Azure SQL Database connection...")

    result = test_azure_sql_connection()

    results_df = pd.DataFrame([result])

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_REPORT, index=False)

    print(results_df)
    print(f"\nConnection test report saved to: {OUTPUT_REPORT}")

    if result["connection_status"] == "success":
        print("\nAzure SQL Database connection successful.")
    else:
        raise RuntimeError("Azure SQL Database connection failed.")


if __name__ == "__main__":
    main()