from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_REPORT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "adf_setup_verification_report.csv"
)

EXPECTED_FILES = [
    "docs/azure_data_factory.md",
    "sql/azure_sql/create_adf_staging_tables.sql",
    "scripts/create_adf_staging_tables.py",
    "scripts/verify_adf_pipeline_output.py",
    "README.md",
    "docs/data_dictionary.md",
    "docs/architecture.md",
    "docs/data_governance.md",
]

EXPECTED_DOC_CONTENT = [
    "Azure Data Factory",
    "pl_copy_olist_orders_blob_to_sql",
    "ls_azure_blob_olist_raw",
    "ls_azure_sql_retail",
    "ds_blob_olist_orders_raw_csv",
    "ds_sql_adf_stg_orders_raw",
    "adf_stg_orders_raw",
]

EXPECTED_README_CONTENT = [
    "Azure Data Factory",
    "pl_copy_olist_orders_blob_to_sql",
    "verify_adf_pipeline_output.py",
]

EXPECTED_ARCHITECTURE_CONTENT = [
    "Azure Data Factory Orchestration Layer",
    "ADF Copy Activity",
    "dbo.adf_stg_orders_raw",
]

EXPECTED_GOVERNANCE_CONTENT = [
    "Azure Data Factory Governance",
    "raw/olist/olist_orders_dataset.csv",
    "avoid duplicate records",
]

EXPECTED_DATA_DICTIONARY_CONTENT = [
    "Azure Data Factory Files and Objects",
    "ADF Staging Table",
    "ADF Pipeline Objects",
]


def read_file_safely(relative_path: str) -> str:
    file_path = PROJECT_ROOT / relative_path

    if not file_path.exists():
        return ""

    encodings = ["utf-8", "utf-8-sig", "utf-16", "cp1252"]

    for encoding in encodings:
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    return file_path.read_text(errors="ignore")


def file_contains(relative_path: str, text: str) -> bool:
    return text in read_file_safely(relative_path)


def main() -> None:
    results = []

    for relative_path in EXPECTED_FILES:
        results.append(
            {
                "check_type": "file_exists",
                "item": relative_path,
                "passed": (PROJECT_ROOT / relative_path).exists(),
            }
        )

    for text in EXPECTED_DOC_CONTENT:
        results.append(
            {
                "check_type": "adf_doc_content",
                "item": text,
                "passed": file_contains("docs/azure_data_factory.md", text),
            }
        )

    for text in EXPECTED_README_CONTENT:
        results.append(
            {
                "check_type": "readme_content",
                "item": text,
                "passed": file_contains("README.md", text),
            }
        )

    for text in EXPECTED_ARCHITECTURE_CONTENT:
        results.append(
            {
                "check_type": "architecture_content",
                "item": text,
                "passed": file_contains("docs/architecture.md", text),
            }
        )

    for text in EXPECTED_GOVERNANCE_CONTENT:
        results.append(
            {
                "check_type": "governance_content",
                "item": text,
                "passed": file_contains("docs/data_governance.md", text),
            }
        )

    for text in EXPECTED_DATA_DICTIONARY_CONTENT:
        results.append(
            {
                "check_type": "data_dictionary_content",
                "item": text,
                "passed": file_contains("docs/data_dictionary.md", text),
            }
        )

    results_df = pd.DataFrame(results)

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_REPORT, index=False)

    print(results_df)

    failed_checks = results_df[results_df["passed"] == False]

    print(f"\nVerification report saved to: {OUTPUT_REPORT}")

    if failed_checks.empty:
        print("\nADF setup verification passed.")
    else:
        print("\nSome ADF setup checks failed:")
        print(failed_checks[["check_type", "item"]])
        raise RuntimeError("ADF setup verification failed.")


if __name__ == "__main__":
    main()