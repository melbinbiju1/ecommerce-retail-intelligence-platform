from pathlib import Path
from typing import Iterable

from azure.core.exceptions import AzureError, ResourceExistsError
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_blob_config() -> dict:
    """
    Load Azure Blob Storage configuration from environment variables.
    """
    load_dotenv(PROJECT_ROOT / ".env")

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME", "ecommerce-retail-data")
    raw_prefix = os.getenv("AZURE_BLOB_RAW_PREFIX", "raw/olist")

    if not connection_string:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING is missing. "
            "Add it to your local .env file."
        )

    return {
        "connection_string": connection_string,
        "container_name": container_name,
        "raw_prefix": raw_prefix.strip("/"),
    }


def get_blob_service_client() -> BlobServiceClient:
    """
    Create a BlobServiceClient using the Azure Storage connection string.
    """
    config = load_blob_config()
    return BlobServiceClient.from_connection_string(config["connection_string"])


def get_container_client():
    """
    Get the configured Azure Blob container client.
    """
    config = load_blob_config()
    service_client = get_blob_service_client()
    return service_client.get_container_client(config["container_name"])


def create_container_if_not_exists() -> None:
    """
    Create the configured blob container if it does not already exist.
    """
    config = load_blob_config()
    service_client = get_blob_service_client()
    container_client = service_client.get_container_client(config["container_name"])

    try:
        container_client.create_container()
        print(f"Created container: {config['container_name']}")
    except ResourceExistsError:
        print(f"Container already exists: {config['container_name']}")


def upload_file_to_blob(local_file_path: Path, blob_name: str, overwrite: bool = True) -> dict:
    """
    Upload one local file to Azure Blob Storage.
    """
    local_file_path = Path(local_file_path)

    if not local_file_path.exists():
        raise FileNotFoundError(f"Local file not found: {local_file_path}")

    container_client = get_container_client()
    blob_client = container_client.get_blob_client(blob_name)

    try:
        with local_file_path.open("rb") as file_data:
            blob_client.upload_blob(file_data, overwrite=overwrite)

        properties = blob_client.get_blob_properties()

        return {
            "local_file": str(local_file_path),
            "blob_name": blob_name,
            "file_size_bytes": local_file_path.stat().st_size,
            "upload_status": "success",
            "etag": properties.etag,
            "last_modified": properties.last_modified,
        }

    except AzureError as exc:
        return {
            "local_file": str(local_file_path),
            "blob_name": blob_name,
            "file_size_bytes": local_file_path.stat().st_size,
            "upload_status": "failed",
            "error": str(exc),
        }


def list_blobs(prefix: str = "") -> list[dict]:
    """
    List blobs from the configured container.
    """
    container_client = get_container_client()

    blob_records = []
    for blob in container_client.list_blobs(name_starts_with=prefix):
        blob_records.append(
            {
                "blob_name": blob.name,
                "size_bytes": blob.size,
                "last_modified": blob.last_modified,
            }
        )

    return blob_records


def get_raw_csv_files(raw_data_dir: Path) -> Iterable[Path]:
    """
    Return CSV files from the local raw data directory.
    """
    raw_data_dir = Path(raw_data_dir)

    if not raw_data_dir.exists():
        raise FileNotFoundError(f"Raw data directory not found: {raw_data_dir}")

    return sorted(raw_data_dir.glob("*.csv"))