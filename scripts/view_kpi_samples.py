from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


KPI_VIEWS = [
    "vw_executive_summary",
    "vw_monthly_sales",
    "vw_product_performance",
    "vw_seller_performance",
    "vw_customer_state_performance",
    "vw_delivery_performance",
    "vw_payment_analysis",
    "vw_review_analysis",
]


def main() -> None:
    engine = get_engine()

    for view_name in KPI_VIEWS:
        print("\n" + "=" * 100)
        print(f"Sample from {view_name}")
        print("=" * 100)

        query = f"SELECT * FROM {view_name} LIMIT 10"
        df = pd.read_sql(query, engine)
        print(df)


if __name__ == "__main__":
    main()