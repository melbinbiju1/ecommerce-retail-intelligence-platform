from pathlib import Path
import sys
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


DEPRECATED_TABLES = [
    "sim_inventory_policy",
    "sim_stock_movements",
    "sim_inventory_snapshot",
    "inventory_event_log",
    "inventory_event_records",
    "inventory_event_failed_records",
]


def main() -> None:
    engine = get_engine()

    with engine.begin() as connection:
        for table_name in DEPRECATED_TABLES:
            connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            print(f"Dropped table if existed: {table_name}")

    print("\nDeprecated inventory tables removed from database.")


if __name__ == "__main__":
    main()