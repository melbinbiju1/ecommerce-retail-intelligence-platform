from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


TABLES_TO_SAMPLE = [
    "stg_orders",
    "stg_order_items",
    "stg_products",
    "stg_customers",
    "stg_sellers",
]


def main() -> None:
    engine = get_engine()

    for table_name in TABLES_TO_SAMPLE:
        print("\n" + "=" * 80)
        print(f"Sample from {table_name}")
        print("=" * 80)

        query = f"SELECT * FROM {table_name} LIMIT 5"
        df = pd.read_sql(query, engine)
        print(df)


if __name__ == "__main__":
    main()