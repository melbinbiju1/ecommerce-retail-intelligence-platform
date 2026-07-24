# Azure SQL Database

## Purpose

Azure SQL Database is used as the cloud serving database for curated analytical data in the E-Commerce Retail Intelligence Platform.

This phase moves the project beyond local SQLite and prepares the curated data model for cloud-based API and reporting use.

## Role in the Architecture

The project uses Azure SQL Database to store curated serving-layer objects.

The cloud architecture becomes:

```text
Azure Blob Storage
        ↓
Raw Olist CSV files
        ↓
Local/dbt transformation pipeline
        ↓
Curated warehouse and operational outputs
        ↓
Azure SQL Database
        ↓
FastAPI / Power BI serving layer
```

## Local and Cloud Database Design

| Layer | Local Development | Cloud Serving |
|---|---|---|
| Raw files | `data/raw/` | Azure Blob Storage |
| Transformation | SQLite + dbt | Later Azure SQL/dbt-compatible flow |
| Serving database | `retail_intelligence.db` | Azure SQL Database |
| API source | Local SQLite | Later Azure SQL |
| Dashboard source | Power BI CSV exports / SQLite-derived data | Later Azure SQL |

## Azure SQL Objects Loaded

The migration script loads selected curated tables from SQLite into Azure SQL.

### Dimension Tables

| Table | Purpose |
|---|---|
| `dim_date` | Date dimension for analytical filtering |
| `dim_customer` | Customer location and customer identifiers |
| `dim_product` | Product and category attributes |
| `dim_seller` | Seller location and seller identifiers |

### Fact Tables

| Table | Purpose |
|---|---|
| `fact_sales` | Sales order/item-level commercial metrics |
| `fact_delivery` | Delivery performance metrics |
| `fact_payments` | Payment method and payment value metrics |
| `fact_reviews` | Customer review metrics |

### Operational Tables

| Table | Purpose |
|---|---|
| `ops_daily_metrics` | Daily operational KPIs |
| `ops_seller_metrics` | Seller-level operational metrics |
| `ops_category_metrics` | Category-level operational metrics |
| `ops_anomaly_rules` | Anomaly detection rule definitions |
| `ops_anomaly_alerts` | Generated operational anomaly alerts |
| `ops_event_log` | Event pipeline processing log |
| `ops_event_records` | Processed operational event records |

## Migration Script

Curated data is migrated using:

```powershell
python scripts\migrate_curated_data_to_azure_sql.py
```

The script:

1. Reads selected curated objects from `retail_intelligence.db`
2. Cleans dataframe values for SQL Server compatibility
3. Loads objects into Azure SQL under the `dbo` schema
4. Writes a migration report

Migration report:

```text
data/processed/azure_sql_migration_report.csv
```

## Verification Script

Azure SQL setup is verified using:

```powershell
python scripts\verify_azure_sql_setup.py
```

The verification script checks:

- Required local files exist
- Required `.env.example` variables are documented
- Required Python dependencies are present
- Expected Azure SQL tables exist
- Loaded Azure SQL tables contain rows

Verification report:

```text
data/processed/azure_sql_setup_verification_report.csv
```

## Environment Variables

The local `.env` file requires:

```text
AZURE_SQL_SERVER=your-server-name.database.windows.net
AZURE_SQL_DATABASE=sqldb-ecommerce-retail-intelligence
AZURE_SQL_USERNAME=your_sql_admin_username
AZURE_SQL_PASSWORD=your_sql_admin_password
AZURE_SQL_DRIVER=ODBC Driver 18 for SQL Server
```

Real credentials must stay in `.env` only.

They must not be committed to GitHub.

## Security Notes

This phase uses SQL authentication for local development and portfolio demonstration.

In later phases, the project will improve secret management using Azure Key Vault.

Firewall access is restricted by allowing only the current client IP for local development.

## Cost Control

The Azure SQL Database is configured using a low-cost or free-tier option where available.

The free offer behavior should be configured to pause or stop usage when the free monthly limit is reached to avoid unexpected costs.
