# System Flow

> This document explains how data, transformations, API requests, deployment, security, and monitoring flow through the E-Commerce Retail Intelligence Platform.

---

## 1. Purpose

The purpose of this document is to explain the system flow from raw data to cloud-hosted API outputs.

It focuses on how each part of the project connects to the next part.

The complete flow is:

```text
Raw data
    ↓
Local ingestion
    ↓
Data validation
    ↓
Warehouse modelling
    ↓
Operational anomaly detection
    ↓
Cloud storage and orchestration
    ↓
Azure SQL serving
    ↓
FastAPI
    ↓
Azure deployment
    ↓
Security and monitoring
```

---

## 2. High-Level System Flow

```text
Olist CSV files
        ↓
Python ingestion scripts
        ↓
SQLite raw tables
        ↓
Data quality checks
        ↓
Staging models
        ↓
Dimensional warehouse tables
        ↓
Operational KPI and anomaly outputs
        ↓
Azure SQL migration
        ↓
FastAPI endpoints
        ↓
Docker container
        ↓
Azure App Service
        ↓
External API users / dashboard layer
```

---

## 3. Local Data Flow

The local pipeline starts with raw Olist CSV files.

```text
data/raw/
    ↓
Python ingestion
    ↓
retail_intelligence.db
    ↓
raw SQLite tables
```

The goal of the local flow is to make development reproducible and easy to test.

Local SQLite is used because it is:

- Simple to run
- Easy to inspect
- Suitable for a portfolio-scale analytical project
- Useful before moving curated outputs to Azure SQL

---

## 4. Raw Data Ingestion Flow

Raw CSV files are loaded into SQLite using Python scripts.

```text
CSV file
    ↓
pandas read_csv
    ↓
SQLite table
    ↓
row count and schema validation
```

The ingestion layer preserves the original source structure as much as possible.

This allows later layers to apply cleaning and transformation logic in a controlled way.

---

## 5. Data Quality Flow

After ingestion, data quality checks validate whether the source data is usable.

```text
Raw SQLite tables
    ↓
Data quality scripts
    ↓
Validation results
    ↓
Cleaned staging inputs
```

Examples of data quality checks:

- Missing values
- Duplicate identifiers
- Invalid dates
- Unexpected row counts
- Referential integrity issues
- Business rule violations

The purpose is not to force the dataset to be perfect, but to make data issues visible and documented.

---

## 6. Staging Flow

The staging layer prepares raw data for warehouse modelling.

```text
Raw source tables
    ↓
Staging transformations
    ↓
Standardized staging tables
```

Staging transformations include:

- Column renaming
- Type casting
- Date parsing
- Standardized naming conventions
- Basic cleaning
- Removing unnecessary raw complexity

The staging layer gives the warehouse layer cleaner and more reliable inputs.

---

## 7. Warehouse Modelling Flow

The warehouse layer converts staging data into analytical facts and dimensions.

```text
Staging tables
    ↓
Dimension models
    ↓
Fact models
    ↓
Analytical views and KPI outputs
```

Main dimensions:

```text
dim_date
dim_customer
dim_product
dim_seller
```

Main facts:

```text
fact_sales
fact_delivery
fact_payments
fact_reviews
```

This structure supports analytics across:

- Time
- Customers
- Products
- Sellers
- Orders
- Payments
- Deliveries
- Reviews

## Warehouse Relationship Flow

The curated warehouse is built around shared dimensions and transactional fact tables.

```text
dim_customer
dim_product
dim_seller
dim_date
        ↓
fact_sales
fact_delivery
fact_payments
fact_reviews
        ↓
KPI views
        ↓
Operational metrics
        ↓
Anomaly alerts
        ↓
API serving objects
```

This relationship flow allows the platform to support executive metrics, operational risk analysis, and API-ready analytical outputs from the same curated warehouse structure.

## 8. dbt Flow

dbt organizes the transformation layer.

```text
Source / staging SQL
    ↓
dbt models
    ↓
dbt tests
    ↓
dbt documentation and lineage
```

dbt adds analytics engineering practices to the project:

- Modular SQL
- Reusable models
- Schema tests
- Documentation
- Lineage visibility

The dbt layer makes the transformation logic easier to maintain and explain.

---

## 9. KPI Flow

KPI views and serving outputs summarize business performance.

```text
Warehouse facts and dimensions
    ↓
KPI SQL views
    ↓
Executive and operational outputs
```

Example KPI outputs:

- Total revenue
- Order count
- Average order value
- Monthly sales
- Top categories
- Top sellers
- Customer state performance
- Review performance
- Delivery performance

These outputs feed both API endpoints and future dashboard reporting.

---

## 10. Operational Anomaly Detection Flow

The operational intelligence layer detects patterns that may need business attention.

```text
Warehouse tables
    ↓
Operational metrics
    ↓
Anomaly rules
    ↓
Anomaly alerts
    ↓
Event records
```

Example anomaly areas:

- Late delivery risk
- Seller risk
- Category risk
- Review quality issues
- Operational severity patterns

Important outputs:

```text
ops_daily_metrics
ops_seller_metrics
ops_category_metrics
ops_anomaly_rules
ops_anomaly_alerts
ops_event_log
ops_event_records
```

This gives the project an operational monitoring story instead of only a reporting story.

---

## 11. Power BI Export Flow

The Power BI export layer prepares dashboard-ready outputs.

```text
Curated warehouse and KPI outputs
    ↓
Export scripts
    ↓
Dashboard-ready files
```

Power BI dashboard creation is handled later, but the export layer exists so dashboard development can use clean, curated data.

This avoids connecting Power BI directly to raw or intermediate tables.

---

## 12. Azure Blob Storage Flow

Azure Blob Storage acts as the cloud raw data landing zone.

```text
Local raw CSV files
    ↓
Upload script
    ↓
Azure Blob container
    ↓
raw/olist/ folder
```

Cloud storage structure:

```text
ecommerce-retail-data
    ↓
raw/olist/
    ↓
olist CSV files
```

Purpose:

- Store raw files in Azure
- Demonstrate cloud data lake style storage
- Provide source data for Azure Data Factory
- Separate local development from cloud storage

---

## 13. Azure Data Factory Flow

Azure Data Factory orchestrates cloud data movement.

```text
Azure Blob Storage
    ↓
ADF copy pipeline
    ↓
Azure SQL staging table
```

Implemented flow:

```text
raw/olist/olist_orders_dataset.csv
        ↓
pl_copy_olist_orders_blob_to_sql
        ↓
dbo.adf_stg_orders_raw
```

This shows how a cloud orchestration service moves raw data from storage into a cloud database.

---

## 14. Azure SQL Migration Flow

Curated local outputs are migrated into Azure SQL Database.

```text
SQLite curated tables
    ↓
Migration scripts
    ↓
Azure SQL Database tables
```

Azure SQL stores:

- Dimensions
- Facts
- Operational metrics
- Anomaly alerts
- API serving objects
- ADF staging outputs

The deployed API reads from Azure SQL rather than local SQLite.

---

## 15. API Data Flow

The FastAPI backend reads from the serving layer and returns JSON responses.

```text
API client
    ↓
FastAPI route
    ↓
Authentication and RBAC check
    ↓
Database query
    ↓
JSON response
```

For example:

```text
GET /executive/summary
        ↓
Validate X-API-Key
        ↓
Query vw_executive_summary
        ↓
Return executive KPIs as JSON
```

---

## 16. API Runtime Mode Flow

The API supports two runtime modes.

```text
APP_ENV=local
    ↓
SQLite database

APP_ENV=azure
    ↓
Azure SQL Database
```

This design allows:

- Local development with SQLite
- Cloud deployment with Azure SQL
- Same FastAPI codebase across both environments

---

## 17. Authentication and RBAC Flow

Protected API routes require an API key.

```text
Request
    ↓
X-API-Key header
    ↓
API key validation
    ↓
Role detection
    ↓
Route permission check
    ↓
Response or access denied
```

Roles:

| Role | Access |
|---|---|
| Admin | Full API access |
| Analyst | Business, operations, and insights access |
| Viewer | Limited read-only access |

This provides a simple but practical access-control layer.

---

## 18. Docker Build Flow

The API is packaged into a Docker image.

```text
Source code
    ↓
Dockerfile
    ↓
Docker image
    ↓
Local container test
```

The Docker image includes:

- FastAPI app code
- Python dependencies
- Uvicorn server
- Azure SQL ODBC dependencies

The Docker image excludes:

- Local `.env`
- SQLite database
- Virtual environment
- Cache files
- Local-only artifacts

---

## 19. Azure Container Registry Flow

The Docker image is pushed to Azure Container Registry.

```text
Local Docker image
    ↓
Docker tag
    ↓
Azure Container Registry
```

Image path:

```text
acrecommerceretailmelbin.azurecr.io/ecommerce-retail-api:latest
```

Azure App Service pulls this image during deployment.

---

## 20. Azure App Service Deployment Flow

Azure App Service runs the API container.

```text
Azure Container Registry
    ↓
Azure App Service pulls image
    ↓
Container starts
    ↓
Uvicorn serves FastAPI
    ↓
Public HTTPS endpoint becomes available
```

The deployed API URL is:

```text
https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net
```

Runtime setting:

```text
WEBSITES_PORT=8000
```

This tells App Service which port the container listens on.

---

## 21. Managed Identity for Container Pull

Azure App Service uses managed identity to pull the container image from Azure Container Registry.

```text
App Service managed identity
    ↓
AcrPull role on ACR
    ↓
Permission to pull Docker image
```

This avoids storing ACR username/password credentials in App Service.

---

## 22. Azure Key Vault Secret Flow

Sensitive values are stored in Azure Key Vault.

```text
Azure Key Vault
    ↓
Key Vault references in App Service settings
    ↓
Resolved environment variables
    ↓
FastAPI app reads environment variables
```

Secrets include:

- Azure SQL server
- Azure SQL database
- Azure SQL username
- Azure SQL password
- Admin API key
- Analyst API key
- Viewer API key

The FastAPI app does not directly call Key Vault.

Azure App Service resolves the secret references before the app reads them.

---

## 23. Monitoring Flow

Monitoring is handled by App Service logs and Application Insights.

```text
Azure App Service
    ↓
Application logging
    ↓
Log Stream
```

Availability monitoring:

```text
Application Insights
    ↓
Calls /health/
    ↓
Expects HTTP 200
    ↓
Records availability result
    ↓
Alert rule watches failed locations
```

This proves that the deployed API is observable and externally monitored.

---

## 24. Health Check Flow

The health endpoint is public.

```text
GET /health/
    ↓
FastAPI health route
    ↓
Database connection check
    ↓
JSON health response
```

Expected response:

```json
{
  "status": "ok",
  "service": "E-Commerce Retail Intelligence API",
  "database_connected": true
}
```

This endpoint is used by:

- Manual testing
- Monitoring verification scripts
- Application Insights availability tests

---

## 25. Verification Flow

Each major system component has a verification script or report.

```text
Build / configure component
    ↓
Run verification script
    ↓
Generate CSV report
    ↓
Use report as evidence
```

Examples:

| Area | Verification |
|---|---|
| Automated tests | `scripts/run_tests.py` |
| Docker | `scripts/verify_docker_setup.py` |
| Azure Blob | `scripts/verify_azure_blob_setup.py` |
| Azure SQL | `scripts/verify_azure_sql_setup.py` |
| Azure Data Factory | `scripts/verify_adf_setup.py` |
| Azure App Service | `scripts/verify_azure_app_deployment.py` |
| Azure Key Vault | `scripts/verify_key_vault_setup.py` |
| Azure Monitoring | `scripts/verify_azure_monitoring_setup.py` |

---

## 26. End-to-End Request Flow

This is the final cloud request flow after deployment:

```text
User or API client
        ↓
HTTPS request to Azure App Service
        ↓
FastAPI container
        ↓
API key validation
        ↓
RBAC permission check
        ↓
Azure SQL query
        ↓
JSON response
        ↓
Application Insights availability monitoring
```

Example:

```text
GET /operations/alert-summary
        ↓
X-API-Key validated as Admin or Analyst
        ↓
Query operational alert summary serving object
        ↓
Return operational risk metrics
```

---

## 27. End-to-End Data Flow

This is the final data engineering flow:

```text
Olist CSV files
        ↓
Raw ingestion
        ↓
Data quality validation
        ↓
Staging transformations
        ↓
Warehouse facts and dimensions
        ↓
Operational anomaly detection
        ↓
Azure SQL serving layer
        ↓
FastAPI API endpoints
        ↓
Monitoring and verification
```

---

## 28. Final System Flow Summary

The final system has two connected tracks.

### Data engineering track

```text
Raw data
    ↓
Ingestion
    ↓
Validation
    ↓
Warehouse modelling
    ↓
Operational analytics
    ↓
Azure SQL serving
```

### Application/cloud track

```text
FastAPI backend
    ↓
Docker image
    ↓
Azure Container Registry
    ↓
Azure App Service
    ↓
Key Vault secrets
    ↓
Application Insights monitoring
```

Together, these tracks form a complete cloud data platform:

```text
Data pipeline + analytical warehouse + secured API + cloud deployment + monitoring
```

---

## 29. What This Flow Demonstrates

This system flow demonstrates that the project is not a single script or dashboard.

It shows an integrated platform with:

- Reproducible ingestion
- Data validation
- Warehouse modelling
- Analytics engineering
- Operational anomaly detection
- Cloud storage
- Cloud orchestration
- Cloud SQL serving
- API delivery
- Authentication
- Container deployment
- Secret management
- Monitoring and alerting

This is the core technical story of the project.