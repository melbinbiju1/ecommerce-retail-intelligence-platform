from pathlib import Path
import pandas as pd


RAW_DATA_DIR = Path("data/raw")
REPORT_DIR = Path("data/processed")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

EXPECTED_FILES = {
    "olist_customers_dataset.csv": [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ],
    "olist_geolocation_dataset.csv": [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state",
    ],
    "olist_order_items_dataset.csv": [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    ],
    "olist_order_payments_dataset.csv": [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
    ],
    "olist_order_reviews_dataset.csv": [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp",
    ],
    "olist_orders_dataset.csv": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "olist_products_dataset.csv": [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
    "olist_sellers_dataset.csv": [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state",
    ],
    "product_category_name_translation.csv": [
        "product_category_name",
        "product_category_name_english",
    ],
}


def inspect_file(file_name: str, expected_columns: list[str]) -> dict:
    file_path = RAW_DATA_DIR / file_name

    result = {
        "file_name": file_name,
        "file_exists": file_path.exists(),
        "row_count": None,
        "column_count": None,
        "missing_expected_columns": None,
        "extra_columns": None,
        "duplicate_rows": None,
        "total_missing_values": None,
        "status": "NOT_CHECKED",
        "error_message": "",
    }

    if not file_path.exists():
        result["status"] = "FAILED"
        result["error_message"] = "File not found"
        return result

    try:
        df = pd.read_csv(file_path)

        actual_columns = list(df.columns)
        missing_expected_columns = [
            col for col in expected_columns if col not in actual_columns
        ]
        extra_columns = [
            col for col in actual_columns if col not in expected_columns
        ]

        result["row_count"] = len(df)
        result["column_count"] = len(actual_columns)
        result["missing_expected_columns"] = ", ".join(missing_expected_columns)
        result["extra_columns"] = ", ".join(extra_columns)
        result["duplicate_rows"] = int(df.duplicated().sum())
        result["total_missing_values"] = int(df.isna().sum().sum())

        if missing_expected_columns:
            result["status"] = "FAILED"
            result["error_message"] = "Missing expected columns"
        else:
            result["status"] = "PASSED"

        return result

    except Exception as error:
        result["status"] = "FAILED"
        result["error_message"] = str(error)
        return result


def create_column_profile(file_name: str) -> pd.DataFrame:
    file_path = RAW_DATA_DIR / file_name
    df = pd.read_csv(file_path)

    profile_rows = []

    for column in df.columns:
        profile_rows.append(
            {
                "file_name": file_name,
                "column_name": column,
                "data_type": str(df[column].dtype),
                "missing_values": int(df[column].isna().sum()),
                "missing_percentage": round(float(df[column].isna().mean() * 100), 2),
                "unique_values": int(df[column].nunique(dropna=True)),
                "sample_values": ", ".join(
                    df[column].dropna().astype(str).head(3).tolist()
                ),
            }
        )

    return pd.DataFrame(profile_rows)


def main() -> None:
    print("Starting raw data inspection...\n")

    inspection_results = []
    column_profiles = []

    for file_name, expected_columns in EXPECTED_FILES.items():
        print(f"Checking {file_name}...")
        result = inspect_file(file_name, expected_columns)
        inspection_results.append(result)

        if result["file_exists"] and result["status"] in ["PASSED", "FAILED"]:
            try:
                column_profiles.append(create_column_profile(file_name))
            except Exception as error:
                print(f"Could not create profile for {file_name}: {error}")

    inspection_df = pd.DataFrame(inspection_results)

    inspection_report_path = REPORT_DIR / "raw_file_inspection_report.csv"
    inspection_df.to_csv(inspection_report_path, index=False)

    if column_profiles:
        column_profile_df = pd.concat(column_profiles, ignore_index=True)
        column_profile_path = REPORT_DIR / "raw_column_profile_report.csv"
        column_profile_df.to_csv(column_profile_path, index=False)

    print("\nRaw data inspection completed.")
    print(f"Inspection report saved to: {inspection_report_path}")
    print(f"Column profile report saved to: {REPORT_DIR / 'raw_column_profile_report.csv'}")

    print("\nSummary:")
    print(inspection_df[["file_name", "status", "row_count", "column_count", "total_missing_values"]])


if __name__ == "__main__":
    main()