from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


TABLES_TO_SAMPLE = [
    "ops_daily_metrics",
    "ops_seller_metrics",
    "ops_category_metrics",
]


def main() -> None:
    engine = get_engine()

    for table_name in TABLES_TO_SAMPLE:
        print("\n" + "=" * 100)
        print(f"Sample from {table_name}")
        print("=" * 100)

        query = f"SELECT * FROM {table_name} LIMIT 10"
        df = pd.read_sql(query, engine)
        print(df)


if __name__ == "__main__":
    main()