from pathlib import Path
from datetime import datetime
import sys
import pandas as pd
import numpy as np
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


LOG_DIR = Path("logs")
REPORT_DIR = Path("data/processed")
LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def write_log(message: str) -> None:
    log_file = LOG_DIR / "inventory_simulation.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def load_sales_demand(engine) -> pd.DataFrame:
    query = """
    SELECT
        fs.order_id,
        fs.order_item_id,
        dd.full_date AS movement_date,
        dp.product_id,
        ds.seller_id,
        dp.product_category_name_english,
        fs.item_price
    FROM fact_sales fs
    LEFT JOIN dim_date dd
        ON fs.purchase_date_key = dd.date_key
    LEFT JOIN dim_product dp
        ON fs.product_key = dp.product_key
    LEFT JOIN dim_seller ds
        ON fs.seller_key = ds.seller_key
    WHERE dd.full_date IS NOT NULL
      AND dp.product_id IS NOT NULL
      AND ds.seller_id IS NOT NULL
    """

    return pd.read_sql(query, engine)


def create_inventory_policy(demand_df: pd.DataFrame) -> pd.DataFrame:
    product_seller_demand = (
        demand_df.groupby(["product_id", "seller_id", "product_category_name_english"])
        .size()
        .reset_index(name="total_units_sold")
    )

    product_seller_demand["avg_daily_demand"] = (
        product_seller_demand["total_units_sold"] / 365
    ).round(2)

    product_seller_demand["reorder_level"] = np.maximum(
        5,
        np.ceil(product_seller_demand["avg_daily_demand"] * 14)
    ).astype(int)

    product_seller_demand["safety_stock"] = np.maximum(
        3,
        np.ceil(product_seller_demand["avg_daily_demand"] * 7)
    ).astype(int)

    product_seller_demand["initial_stock"] = (
        product_seller_demand["reorder_level"]
        + product_seller_demand["safety_stock"]
        + np.maximum(10, product_seller_demand["total_units_sold"] * 0.20).astype(int)
    )

    product_seller_demand["lead_time_days"] = 7
    product_seller_demand["policy_created_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return product_seller_demand


def create_stock_movements(demand_df: pd.DataFrame, policy_df: pd.DataFrame) -> pd.DataFrame:
    sales_movements = (
        demand_df.groupby(["movement_date", "product_id", "seller_id"])
        .size()
        .reset_index(name="quantity")
    )

    sales_movements["movement_type"] = "SALE"
    sales_movements["quantity_change"] = -sales_movements["quantity"]
    sales_movements["reason"] = "Customer order demand from Olist order items"

    first_sale_date = (
        sales_movements.groupby(["product_id", "seller_id"])["movement_date"]
        .min()
        .reset_index()
        .rename(columns={"movement_date": "first_sale_date"})
    )

    restock_movements = policy_df.merge(
        first_sale_date,
        on=["product_id", "seller_id"],
        how="left"
    )

    restock_movements["movement_date"] = restock_movements["first_sale_date"]
    restock_movements["movement_type"] = "INITIAL_STOCK"
    restock_movements["quantity"] = restock_movements["initial_stock"]
    restock_movements["quantity_change"] = restock_movements["initial_stock"]
    restock_movements["reason"] = "Initial stock generated from demand-based inventory policy"

    restock_movements = restock_movements[
        [
            "movement_date",
            "product_id",
            "seller_id",
            "quantity",
            "movement_type",
            "quantity_change",
            "reason",
        ]
    ]

    combined_movements = pd.concat(
        [
            restock_movements,
            sales_movements[
                [
                    "movement_date",
                    "product_id",
                    "seller_id",
                    "quantity",
                    "movement_type",
                    "quantity_change",
                    "reason",
                ]
            ],
        ],
        ignore_index=True,
    )

    combined_movements["movement_date"] = pd.to_datetime(combined_movements["movement_date"])
    combined_movements = combined_movements.sort_values(
        ["product_id", "seller_id", "movement_date", "movement_type"]
    )

    combined_movements.insert(
        0,
        "movement_id",
        range(1, len(combined_movements) + 1)
    )

    combined_movements["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return combined_movements


def create_inventory_snapshot(movements_df: pd.DataFrame, policy_df: pd.DataFrame) -> pd.DataFrame:
    snapshot_df = movements_df.copy()

    snapshot_df["stock_on_hand"] = (
        snapshot_df.groupby(["product_id", "seller_id"])["quantity_change"]
        .cumsum()
    )

    snapshot_df = snapshot_df.merge(
        policy_df[
            [
                "product_id",
                "seller_id",
                "product_category_name_english",
                "reorder_level",
                "safety_stock",
                "lead_time_days",
                "avg_daily_demand",
            ]
        ],
        on=["product_id", "seller_id"],
        how="left",
    )

    snapshot_df["stockout_flag"] = np.where(snapshot_df["stock_on_hand"] <= 0, 1, 0)

    snapshot_df["reorder_flag"] = np.where(
        snapshot_df["stock_on_hand"] <= snapshot_df["reorder_level"],
        1,
        0,
    )

    snapshot_df["days_of_stock_remaining"] = np.where(
        snapshot_df["avg_daily_demand"] > 0,
        (snapshot_df["stock_on_hand"] / snapshot_df["avg_daily_demand"]).round(2),
        None,
    )

    snapshot_df["inventory_risk_level"] = np.select(
        [
            snapshot_df["stock_on_hand"] <= 0,
            snapshot_df["stock_on_hand"] <= snapshot_df["safety_stock"],
            snapshot_df["stock_on_hand"] <= snapshot_df["reorder_level"],
        ],
        [
            "stockout",
            "high",
            "medium",
        ],
        default="low",
    )

    snapshot_df = snapshot_df.rename(columns={"movement_date": "snapshot_date"})

    snapshot_df.insert(
        0,
        "snapshot_id",
        range(1, len(snapshot_df) + 1)
    )

    snapshot_columns = [
        "snapshot_id",
        "snapshot_date",
        "product_id",
        "seller_id",
        "product_category_name_english",
        "stock_on_hand",
        "reorder_level",
        "safety_stock",
        "lead_time_days",
        "avg_daily_demand",
        "days_of_stock_remaining",
        "stockout_flag",
        "reorder_flag",
        "inventory_risk_level",
        "created_at",
    ]

    return snapshot_df[snapshot_columns]


def save_tables(engine, policy_df, movements_df, snapshot_df) -> None:
    policy_df.to_sql("sim_inventory_policy", engine, if_exists="replace", index=False)
    movements_df.to_sql("sim_stock_movements", engine, if_exists="replace", index=False)
    snapshot_df.to_sql("sim_inventory_snapshot", engine, if_exists="replace", index=False)


def create_simulation_report(policy_df, movements_df, snapshot_df) -> None:
    report = {
        "inventory_policy_rows": len(policy_df),
        "stock_movement_rows": len(movements_df),
        "inventory_snapshot_rows": len(snapshot_df),
        "unique_products": policy_df["product_id"].nunique(),
        "unique_sellers": policy_df["seller_id"].nunique(),
        "stockout_records": int(snapshot_df["stockout_flag"].sum()),
        "reorder_records": int(snapshot_df["reorder_flag"].sum()),
        "high_risk_records": int((snapshot_df["inventory_risk_level"] == "high").sum()),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    report_df = pd.DataFrame([report])
    report_path = REPORT_DIR / "inventory_simulation_report.csv"
    report_df.to_csv(report_path, index=False)


def main() -> None:
    print("Starting inventory simulation...")

    engine = get_engine()

    try:
        demand_df = load_sales_demand(engine)
        print(f"Loaded sales demand rows: {len(demand_df)}")

        policy_df = create_inventory_policy(demand_df)
        print(f"Created inventory policy rows: {len(policy_df)}")

        movements_df = create_stock_movements(demand_df, policy_df)
        print(f"Created stock movement rows: {len(movements_df)}")

        snapshot_df = create_inventory_snapshot(movements_df, policy_df)
        print(f"Created inventory snapshot rows: {len(snapshot_df)}")

        save_tables(engine, policy_df, movements_df, snapshot_df)
        create_simulation_report(policy_df, movements_df, snapshot_df)

        write_log("SUCCESS | Inventory simulation completed")
        print("Inventory simulation completed successfully.")
        print("Tables created:")
        print("- sim_inventory_policy")
        print("- sim_stock_movements")
        print("- sim_inventory_snapshot")
        print("Report created: data/processed/inventory_simulation_report.csv")

    except Exception as error:
        write_log(f"FAILED | Inventory simulation failed | {error}")
        print(f"Inventory simulation failed: {error}")
        raise


if __name__ == "__main__":
    main()