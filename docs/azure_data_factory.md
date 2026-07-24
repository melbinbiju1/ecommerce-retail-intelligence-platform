# Azure Data Factory

## Purpose

Azure Data Factory is used as the cloud orchestration layer for the E-Commerce Retail Intelligence Platform.

This phase demonstrates how raw data stored in Azure Blob Storage can be moved into Azure SQL Database using an Azure Data Factory pipeline.

## Role in the Architecture

Azure Data Factory connects the cloud landing zone and cloud serving database.

```text
Azure Blob Storage
        ↓
Azure Data Factory pipeline
        ↓
Azure SQL Database
```

## Data Factory Resource

| Item | Value |
|---|---|
| Data Factory | `adf-ecommerce-retail-intelligence` |
| Pipeline | `pl_copy_olist_orders_blob_to_sql` |
| Copy activity | `copy_olist_orders_to_sql` |
| Source | Azure Blob Storage |
| Sink | Azure SQL Database |

## Linked Services

| Linked Service | Type | Purpose |
|---|---|---|
| `ls_azure_blob_olist_raw` | Azure Blob Storage | Connects ADF to the raw Olist files in Blob Storage |
| `ls_azure_sql_retail` | Azure SQL Database | Connects ADF to the Azure SQL serving database |

## Datasets

| Dataset | Type | Purpose |
|---|---|---|
| `ds_blob_olist_orders_raw_csv` | DelimitedText | Reads `olist_orders_dataset.csv` from `raw/olist/` |
| `ds_sql_adf_stg_orders_raw` | Azure SQL Database | Writes copied order data into `dbo.adf_stg_orders_raw` |

## Pipeline Design

The pipeline copies:

```text
ecommerce-retail-data/raw/olist/olist_orders_dataset.csv
```

into:

```text
dbo.adf_stg_orders_raw
```

The sink table is truncated before each copy run to avoid duplicate records.

## Azure SQL Staging Table

The ADF pipeline writes to:

```text
dbo.adf_stg_orders_raw
```

This table is used to demonstrate Blob-to-SQL cloud orchestration.

It is separate from the curated warehouse tables so that raw ingestion testing does not overwrite the analytical serving model.

## Verification

ADF pipeline output is verified using:

```powershell
python scripts\verify_adf_pipeline_output.py
```

Verification report:

```text
data/processed/adf_pipeline_output_verification_report.csv
```

The script checks:

- Row count
- Distinct order count
- Minimum order purchase timestamp
- Maximum order purchase timestamp

## Governance Notes

This ADF phase uses a simple copy pipeline for proof of cloud orchestration.

The pipeline does not replace the local Python/dbt transformation pipeline yet.

Future improvements can include:

- Metadata-driven copy pipelines
- Multiple raw dataset ingestion
- Scheduled triggers
- Parameterised datasets
- Azure Key Vault integration
- Azure Monitor alerts
