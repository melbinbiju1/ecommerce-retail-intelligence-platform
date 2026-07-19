from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cloud.azure_blob_storage import (  # noqa: E402
    create_container_if_not_exists,
    get_raw_csv_files,
    load_blob_config,
    upload_file_to_blob,
)


RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_REPORT = PROJECT_ROOT / "data" / "processed" / "azure_blob_upload_report.csv"


def main() -> None:
    config = load_blob_config()

    print("Azure Blob upload started.")
    print(f"Container: {config['container_name']}")
    print(f"Raw prefix: {config['raw_prefix']}")

    create_container_if_not_exists()

    upload_results = []

    for file_path in get_raw_csv_files(RAW_DATA_DIR):
        blob_name = f"{config['raw_prefix']}/{file_path.name}"

        print(f"Uploading {file_path.name} -> {blob_name}")

        result = upload_file_to_blob(
            local_file_path=file_path,
            blob_name=blob_name,
            overwrite=True,
        )

        upload_results.append(result)

    results_df = pd.DataFrame(upload_results)

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_REPORT, index=False)

    print(f"\nUpload report saved to: {OUTPUT_REPORT}")

    failed_uploads = results_df[results_df["upload_status"] != "success"]

    if failed_uploads.empty:
        print("Azure Blob raw data upload completed successfully.")
    else:
        print("Some files failed to upload:")
        print(failed_uploads[["local_file", "blob_name", "upload_status"]])
        raise RuntimeError("Azure Blob upload completed with failures.")


if __name__ == "__main__":
    main()