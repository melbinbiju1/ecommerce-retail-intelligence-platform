from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cloud.azure_blob_storage import list_blobs, load_blob_config  # noqa: E402


EXPECTED_LOCAL_FILES = [
    "src/cloud/__init__.py",
    "src/cloud/azure_blob_storage.py",
    "scripts/upload_raw_data_to_blob.py",
    "scripts/verify_azure_blob_setup.py",
    "docs/azure_blob_storage.md",
    ".env.example",
    "requirements.txt",
]

EXPECTED_ENV_EXAMPLE_CONTENT = [
    "AZURE_STORAGE_CONNECTION_STRING",
    "AZURE_BLOB_CONTAINER_NAME",
    "AZURE_BLOB_RAW_PREFIX",
]

EXPECTED_REQUIREMENTS_CONTENT = [
    "azure-storage-blob",
    "python-dotenv",
]

EXPECTED_DOCUMENTATION_CONTENT = [
    "Azure Blob Storage",
    "raw/olist",
    "ecommerce-retail-data",
    "connection string",
    "Azure SQL Database",
    "Azure Key Vault",
]

EXPECTED_RAW_FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]


def read_text_safely(file_path: Path) -> str:
    """
    Read text files using common encodings.
    This avoids failures when a file is saved as UTF-8, UTF-16, or Windows encoding.
    """
    encodings = ["utf-8", "utf-8-sig", "utf-16", "cp1252"]

    for encoding in encodings:
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    return file_path.read_text(errors="ignore")


def file_contains(relative_path: str, text: str) -> bool:
    file_path = PROJECT_ROOT / relative_path

    if not file_path.exists():
        return False

    return text in read_text_safely(file_path)


def main() -> None:
    results = []

    for relative_path in EXPECTED_LOCAL_FILES:
        file_path = PROJECT_ROOT / relative_path
        results.append(
            {
                "check_type": "local_file_exists",
                "item": relative_path,
                "passed": file_path.exists(),
            }
        )

    for text in EXPECTED_ENV_EXAMPLE_CONTENT:
        results.append(
            {
                "check_type": "env_example_content",
                "item": text,
                "passed": file_contains(".env.example", text),
            }
        )

    for text in EXPECTED_REQUIREMENTS_CONTENT:
        results.append(
            {
                "check_type": "requirements_content",
                "item": text,
                "passed": file_contains("requirements.txt", text),
            }
        )

    for text in EXPECTED_DOCUMENTATION_CONTENT:
        results.append(
            {
                "check_type": "azure_blob_doc_content",
                "item": text,
                "passed": file_contains("docs/azure_blob_storage.md", text),
            }
        )

    config = load_blob_config()
    blob_prefix = config["raw_prefix"]

    uploaded_blobs = list_blobs(prefix=blob_prefix)
    uploaded_blob_names = {Path(blob["blob_name"]).name for blob in uploaded_blobs}

    for expected_file in EXPECTED_RAW_FILES:
        results.append(
            {
                "check_type": "blob_raw_file_uploaded",
                "item": expected_file,
                "passed": expected_file in uploaded_blob_names,
            }
        )

    results_df = pd.DataFrame(results)

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "azure_blob_setup_verification_report.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    print(results_df)

    failed_checks = results_df[results_df["passed"] == False]

    print(f"\nVerification report saved to: {output_path}")

    if failed_checks.empty:
        print("\nAzure Blob setup verification passed.")
    else:
        print("\nSome Azure Blob setup checks failed:")
        print(failed_checks[["check_type", "item"]])
        raise RuntimeError("Azure Blob setup verification failed.")


if __name__ == "__main__":
    main()