# Azure Blob Storage

## Purpose

Azure Blob Storage is used as the cloud landing zone for the raw Olist e-commerce CSV files.

This phase moves the project from a purely local data setup toward a cloud-ready data engineering architecture.

## Storage Design

The project uses one Azure Storage container:

```text
ecommerce-retail-data
```

The raw Olist files are uploaded under:

```text
raw/olist/
```

Recommended cloud structure:

```text
ecommerce-retail-data/
    raw/
        olist/
            olist_customers_dataset.csv
            olist_geolocation_dataset.csv
            olist_order_items_dataset.csv
            olist_order_payments_dataset.csv
            olist_order_reviews_dataset.csv
            olist_orders_dataset.csv
            olist_products_dataset.csv
            olist_sellers_dataset.csv
            product_category_name_translation.csv
    processed/
    exports/
    logs/
```

## Files Uploaded

The following raw CSV files are uploaded to Azure Blob Storage:

| File | Purpose |
|---|---|
| `olist_customers_dataset.csv` | Customer and customer location data |
| `olist_geolocation_dataset.csv` | Brazilian geolocation reference data |
| `olist_order_items_dataset.csv` | Order item-level sales data |
| `olist_order_payments_dataset.csv` | Payment method and payment value data |
| `olist_order_reviews_dataset.csv` | Customer review data |
| `olist_orders_dataset.csv` | Order lifecycle and delivery status data |
| `olist_products_dataset.csv` | Product catalogue data |
| `olist_sellers_dataset.csv` | Seller location data |
| `product_category_name_translation.csv` | Product category translation mapping |

## Authentication Design

For this local portfolio phase, the Python upload script uses an Azure Storage connection string stored in the local `.env` file.

The `.env` file is ignored by Git and must not be pushed to GitHub.

The connection string variable is:

```text
AZURE_STORAGE_CONNECTION_STRING
```

In a later production-style phase, secrets will be moved to Azure Key Vault.

## Environment Variables

The following variables are required locally:

```text
AZURE_STORAGE_CONNECTION_STRING=your_azure_storage_connection_string_here
AZURE_BLOB_CONTAINER_NAME=ecommerce-retail-data
AZURE_BLOB_RAW_PREFIX=raw/olist
```

## Upload Script

Raw files are uploaded using:

```powershell
python scripts\upload_raw_data_to_blob.py
```

The script:

1. Loads Azure Blob configuration from `.env`
2. Creates the container if it does not already exist
3. Reads CSV files from `data/raw`
4. Uploads them to `raw/olist/`
5. Writes an upload report

Upload report:

```text
data/processed/azure_blob_upload_report.csv
```

## Verification Script

Azure Blob setup is verified using:

```powershell
python scripts\verify_azure_blob_setup.py
```

The verification script checks:

- Required local files exist
- Required environment variables are documented
- Required Python dependencies are present
- Azure Blob documentation exists
- Expected raw CSV files are uploaded to Azure Blob Storage

Verification report:

```text
data/processed/azure_blob_setup_verification_report.csv
```

## Governance Notes

Raw files are stored in a dedicated cloud landing zone.

The raw area should be treated as immutable source data.

Downstream transformations should read from raw files and write curated outputs to warehouse or processed layers.

The local SQLite database is not uploaded to Azure Blob Storage.

In later phases, Azure Data Factory can use this raw Blob Storage location as a pipeline source, and Azure SQL Database can be used as the curated serving layer.

## Local vs Cloud

| Area | Local Version | Azure Blob Version |
|---|---|---|
| Raw data storage | `data/raw/` | `ecommerce-retail-data/raw/olist/` |
| Upload method | Manual local files | Python Azure Blob upload script |
| Secrets | Local `.env` | Later Azure Key Vault |
| Database | SQLite | Later Azure SQL Database |
| Pipeline orchestration | Local scripts | Later Azure Data Factory |

## Interview Explanation

A simple interview explanation for this phase:

```text
I added Azure Blob Storage as the cloud landing zone for the raw e-commerce dataset. I created a private container, uploaded the raw Olist CSV files under a structured raw/olist path, and built Python scripts to upload and verify the files. This prepares the project for Azure Data Factory ingestion and Azure SQL Database loading in later phases.
```