# Technical Architecture

> This document explains the technical design decisions, components, runtime modes, and engineering patterns used in the E-Commerce Retail Intelligence Platform.

---

## 1. Purpose

The purpose of this document is to describe the technical architecture behind the project.

This document focuses on:

- Why each technology was used
- How the components interact
- How local and cloud modes differ
- How data moves through the system
- How the API is secured and deployed
- How the platform is verified and monitored

For the complete final architecture summary, see:

```text
docs/final_architecture.md
```

For system flow diagrams and request/data movement, see:

```text
docs/system_flow.md
```

---

## 2. Technical Architecture Summary

The platform combines data engineering, analytics engineering, API development, cloud deployment, and monitoring.

```text
Python + SQL + dbt
        ↓
SQLite local warehouse
        ↓
Azure Blob Storage + Azure Data Factory
        ↓
Azure SQL Database
        ↓
FastAPI secured backend
        ↓
Docker + Azure App Service
        ↓
Azure Key Vault + Application Insights
```

The architecture is designed to be:

- Reproducible locally
- Deployable to Azure
- Secure enough for a portfolio API
- Easy to verify with scripts
- Clear to explain in interviews

---

## 3. Main Technical Components

| Component | Technology | Responsibility |
|---|---|---|
| Raw data source | Olist CSV files | Provides e-commerce transactional data |
| Local database | SQLite | Local development warehouse |
| Ingestion | Python, pandas | Loads raw CSV files |
| Transformation | SQL, dbt | Builds staging, warehouse, and mart-style models |
| Data quality | Python, SQL, dbt tests | Validates data reliability |
| Cloud storage | Azure Blob Storage | Stores raw files in Azure |
| Cloud orchestration | Azure Data Factory | Copies cloud raw data into Azure SQL staging |
| Cloud database | Azure SQL Database | Serves curated data to deployed API |
| API backend | FastAPI | Exposes metrics and insights |
| API security | API keys, RBAC | Protects endpoints by role |
| Containerization | Docker | Packages API for deployment |
| Image registry | Azure Container Registry | Stores deployable API image |
| App hosting | Azure App Service | Runs FastAPI container |
| Secret management | Azure Key Vault | Stores SQL credentials and API keys |
| Monitoring | Application Insights | Tracks API availability |
| CI | GitHub Actions | Validates code, imports, Docker build, and project structure |

---

## 4. Local Development Architecture

The local architecture is used for development, testing, and transformation work.

```text
Raw CSV files
    ↓
Python ingestion
    ↓
SQLite database
    ↓
SQL/dbt transformations
    ↓
Operational anomaly detection
    ↓
FastAPI local API
    ↓
Automated tests
```

SQLite is used locally because it keeps the project simple and reproducible. It avoids requiring cloud services for every development task.

Local mode is controlled by:

```env
APP_ENV=local
```

When `APP_ENV` is missing or set to `local`, the API uses the local SQLite database.

---

## 5. Cloud Runtime Architecture

The cloud architecture is used by the deployed API and Azure services.

```text
Azure Blob Storage
    ↓
Azure Data Factory
    ↓
Azure SQL Database
    ↓
Azure App Service FastAPI container
    ↓
Application Insights monitoring
```

Cloud mode is controlled by:

```env
APP_ENV=azure
```

When `APP_ENV=azure`, the API uses Azure SQL Database instead of SQLite.

This allows one FastAPI codebase to support both local and cloud runtime environments.

---

## 6. Runtime Mode Design

The API database connection is environment-driven.

```text
APP_ENV=local
    ↓
Use SQLite

APP_ENV=azure
    ↓
Use Azure SQL Database
```

This design provides:

- Simple local development
- Cloud deployment readiness
- Reduced code duplication
- Clear environment separation

The API database utility decides which engine to use based on the environment variable.

---

## 7. Data Engineering Design

The data engineering layer follows a staged pipeline approach.

```text
Raw
    ↓
Validated
    ↓
Staged
    ↓
Curated
    ↓
Served
```

### Raw

Stores source data close to its original format.

### Validated

Runs checks for completeness, duplicates, date quality, and referential quality.

### Staged

Standardizes raw inputs and prepares them for modelling.

### Curated

Builds facts, dimensions, KPI views, and operational metrics.

### Served

Exposes curated outputs through API endpoints and cloud database tables.

---

## 8. Dimensional Modelling Design

The warehouse uses a star-schema style design.

Dimensions:

```text
dim_date
dim_customer
dim_product
dim_seller
```

Facts:

```text
fact_sales
fact_delivery
fact_payments
fact_reviews
```

This design allows metrics to be analyzed by:

- Date
- Customer
- Product
- Seller
- Geography
- Delivery status
- Review score
- Payment type

The dimensional model makes the project easier to query, document, and explain.

## Database Modelling Design

The warehouse uses a star-schema style design.

The main dimensions describe the business entities:

| Dimension | Description |
|---|---|
| `dim_date` | Calendar attributes for date-based analysis |
| `dim_customer` | Customer geography and customer identifiers |
| `dim_product` | Product and category attributes |
| `dim_seller` | Seller geography and seller identifiers |

The main fact tables capture business events and measurable outcomes:

| Fact Table | Description |
|---|---|
| `fact_sales` | Order item sales, price, freight, product, seller, and customer relationships |
| `fact_delivery` | Order delivery status, delivery duration, delays, and late-delivery flags |
| `fact_payments` | Payment type, installments, sequence, and payment value |
| `fact_reviews` | Review scores and review timing |

This modelling approach separates descriptive attributes from measurable business events. It makes the warehouse easier to query, test, and explain.

## 9. Analytics Engineering Design with dbt

dbt is used to structure the transformation layer.

dbt provides:

- Model organization
- SQL modularity
- Data tests
- Documentation
- Lineage
- Repeatable transformation logic

The dbt layer improves the project from simple SQL scripting to analytics engineering practice.

Typical dbt structure:

```text
dbt_retail/
    models/
        staging/
        marts/
    tests/
    dbt_project.yml
```

---

## 10. Operational Intelligence Design

The operational anomaly layer converts warehouse outputs into operational risk signals.

```text
Warehouse tables
    ↓
Operational metrics
    ↓
Anomaly rules
    ↓
Alert records
    ↓
Event records
```

This design provides a business reason for the project beyond simple reporting.

It supports questions such as:

- Which sellers show higher operational risk?
- Which product categories are associated with delivery or review problems?
- How many alerts are high severity?
- What types of operational anomalies occur most often?

This helps position the project as a retail intelligence and operations monitoring platform.

---

## 11. API Architecture

The API is built with FastAPI.

Main route groups:

```text
/health
/executive
/operations
/insights
```

The API is designed around curated serving objects rather than raw tables.

This keeps API responses:

- Business-friendly
- Smaller and faster
- Easier to test
- Easier to secure
- Easier to consume by dashboards or clients

Example request flow:

```text
Client request
    ↓
FastAPI route
    ↓
Authentication dependency
    ↓
RBAC permission check
    ↓
Database query
    ↓
JSON response
```

---

## 12. API Security Architecture

The API uses API key authentication with role-based access control.

```text
X-API-Key
    ↓
Key validation
    ↓
Role assignment
    ↓
Endpoint permission check
```

Roles:

| Role | Access Pattern |
|---|---|
| Admin | Full access |
| Analyst | Business, operations, and insights access |
| Viewer | Limited read-only access |

This is intentionally simple and appropriate for a portfolio API.

The project avoids hardcoding API keys in source code. In Azure, API keys are stored in Key Vault and injected through App Service settings.

---

## 13. AI-Ready Insights Architecture

The AI-ready insights layer prepares structured business summaries that can be passed to an LLM or used directly by applications.

This layer does not require a paid LLM API to demonstrate value.

It creates:

- Executive summaries
- Sales performance summaries
- Operational risk summaries
- Recommendation-style outputs
- LLM context payloads

Design flow:

```text
Curated KPI and operational outputs
    ↓
Insight generation logic
    ↓
Structured text/JSON outputs
    ↓
API insight endpoints
```

This demonstrates how the platform could support business insight automation.

---

## 14. Docker Architecture

Docker packages the FastAPI application for consistent deployment.

The Docker image includes:

- Python runtime
- FastAPI source code
- Python dependencies
- Uvicorn
- ODBC dependencies for Azure SQL
- Microsoft ODBC Driver 18 for SQL Server

The Docker image excludes:

- `.env`
- SQLite database
- local virtual environment
- cache files
- Git metadata
- Power BI files

The container starts with:

```text
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

---

## 15. Azure Container Registry Architecture

Azure Container Registry stores the deployable Docker image.

```text
Docker build
    ↓
Docker tag
    ↓
Docker push
    ↓
Azure Container Registry
```

Registry:

```text
acrecommerceretailmelbin.azurecr.io
```

Image:

```text
ecommerce-retail-api:latest
```

Azure App Service pulls the image from ACR using managed identity.

---

## 16. Azure App Service Architecture

Azure App Service runs the API as a Linux container.

```text
Azure App Service
    ↓
Pull image from ACR
    ↓
Start FastAPI container
    ↓
Expose HTTPS endpoint
```

Important app settings:

```env
APP_ENV=azure
WEBSITES_PORT=8000
AZURE_SQL_DRIVER=ODBC Driver 18 for SQL Server
```

Secret app settings are resolved from Azure Key Vault references.

---

## 17. Managed Identity Architecture

The App Service uses system-assigned managed identity.

Managed identity is used for:

```text
App Service
    ↓
AcrPull role
    ↓
Azure Container Registry
```

This allows the Web App to pull the image securely without storing registry credentials.

The same App Service identity is also allowed to read secrets from Key Vault.

```text
App Service managed identity
    ↓
Key Vault Secrets User role
    ↓
Azure Key Vault
```

---

## 18. Azure Key Vault Architecture

Azure Key Vault stores sensitive runtime values.

Secrets include:

```text
azure-sql-server
azure-sql-database
azure-sql-username
azure-sql-password
admin-api-key
analyst-api-key
viewer-api-key
```

App Service uses Key Vault reference syntax:

```text
@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=secret-name)
```

At runtime:

```text
App Service resolves Key Vault reference
    ↓
Environment variable becomes available
    ↓
FastAPI reads value using os.getenv()
```

This keeps secrets out of:

- Source code
- GitHub
- Docker image
- Documentation
- Plain App Service configuration values

---

## 19. Azure SQL Architecture

Azure SQL Database is the cloud serving database.

It stores:

- Dimension tables
- Fact tables
- Operational metric tables
- Anomaly alert tables
- API serving objects
- ADF staging tables

The FastAPI app connects to Azure SQL using SQLAlchemy and pyodbc.

Connection inputs are provided through environment variables.

```text
AZURE_SQL_SERVER
AZURE_SQL_DATABASE
AZURE_SQL_USERNAME
AZURE_SQL_PASSWORD
AZURE_SQL_DRIVER
```

In Azure, these values are stored or resolved through Key Vault references.

---

## 20. Azure Blob Storage Architecture

Azure Blob Storage stores the raw source files in the cloud.

```text
Storage account
    ↓
Private container
    ↓
raw/olist/
    ↓
CSV files
```

Blob Storage provides the cloud landing zone for the data.

It is also the source system for the Azure Data Factory copy pipeline.

---

## 21. Azure Data Factory Architecture

Azure Data Factory provides cloud orchestration.

Implemented pipeline:

```text
Azure Blob CSV
    ↓
ADF Copy Activity
    ↓
Azure SQL staging table
```

Pipeline:

```text
pl_copy_olist_orders_blob_to_sql
```

Source:

```text
raw/olist/olist_orders_dataset.csv
```

Sink:

```text
dbo.adf_stg_orders_raw
```

ADF demonstrates the ability to move cloud data between storage and database services using a managed orchestration tool.

---

## 22. Monitoring Architecture

Monitoring is handled through Azure App Service logs and Application Insights.

```text
Azure App Service
    ↓
Application logs
    ↓
Log Stream
```

Availability testing:

```text
Application Insights
    ↓
Calls /health/
    ↓
Expects HTTP 200
    ↓
Records success/failure
    ↓
Alert rule evaluates failures
```

Availability test:

```text
fastapi-health-check
```

The built-in App Service Health Check feature was skipped because the project uses the Free App Service plan.

Application Insights availability testing is used instead.

---

## 23. CI Architecture

GitHub Actions is used to validate the project on every push.

CI checks include:

- Database file is not tracked
- Python dependencies install
- Python files compile
- Key imports work
- Docker setup validation runs
- CI setup validation runs
- Docker image builds successfully

The CI workflow avoids depending on the large local SQLite database.

This makes the workflow faster and more reliable for GitHub.

---

## 24. Testing Architecture

The project includes automated tests for:

- Database utilities
- API health routes
- Executive endpoints
- Operations endpoints
- Insights endpoints
- RBAC permissions
- Pipeline outputs

Test runner:

```powershell
python scripts\run_tests.py
```

Test output:

```text
data/processed/automated_test_run_summary.csv
```

This helps prove that the API and pipeline logic are not only manually tested.

---

## 25. Verification Architecture

In addition to automated tests, each cloud phase has verification scripts.

The verification pattern is:

```text
Configure component
    ↓
Run verification script
    ↓
Generate CSV evidence report
    ↓
Commit documentation and verification outputs
```

This pattern is used for:

- Azure Blob Storage
- Azure SQL Database
- Azure Data Factory
- Azure App Service
- Azure Key Vault
- Azure Monitoring

This makes the project easy to audit and explain.

---

## 26. Configuration Architecture

The project uses environment variables for configuration.

Local secrets are stored in:

```text
.env
```

Safe placeholder examples are stored in:

```text
.env.example
```

The `.env` file must not be committed.

Important configuration groups:

- API keys
- Azure SQL settings
- Azure Blob settings
- Azure App Service URL
- Azure Key Vault name
- Monitoring resource names

This keeps runtime settings separate from source code.

---

## 27. Repository Architecture

The repository is organized by responsibility.

Typical structure:

```text
src/
    api/
    cloud/
    pipeline/
    utils/

scripts/
    ingestion
    migration
    verification
    testing

dbt_retail/
    models
    tests
    documentation

docs/
    setup
    architecture
    governance
    cloud documentation

data/
    raw
    processed
    exports

tests/
    unit
    api
    integration
```

This separation makes the project easier to navigate.

---

## 28. Security Design Decisions

Security decisions:

| Decision | Reason |
|---|---|
| `.env` ignored by Git | Prevent local secrets from being committed |
| Key Vault for cloud secrets | Avoid plain secret values in App Service settings |
| API keys for protected routes | Simple portfolio authentication |
| RBAC roles | Demonstrates access control logic |
| Managed identity for ACR pull | Avoid registry credentials |
| No SQLite DB inside Docker image | Avoid shipping large/local state |
| No secrets in Docker image | Keeps image reusable and safer |

---

## 29. Cost-Aware Design Decisions

This project is designed to demonstrate cloud skills while controlling Azure cost.

Cost-aware choices:

| Choice | Reason |
|---|---|
| Free App Service plan | Avoid unnecessary hosting cost |
| SQLite for local development | Avoid always-on cloud database during development |
| Azure SQL free/serverless-style configuration | Reduce database cost |
| Application Insights availability instead of App Service Health Check | Avoid scaling up only for health check |
| Small ADF demo pipeline | Demonstrate orchestration without large data movement cost |
| Manual image push | Avoid extra deployment automation complexity early |

---

## 30. Scalability Considerations

The current architecture is suitable for a portfolio-scale project.

Potential future scaling improvements:

- Move from SQLite local development to full cloud development database
- Add incremental ingestion
- Add CI/CD container deployment from GitHub Actions
- Add more ADF pipelines
- Add Azure Monitor dashboards or workbooks
- Add more structured application telemetry
- Add production identity provider instead of API keys
- Add caching for high-traffic API endpoints
- Add Power BI dashboard refresh integration

These are future improvements, not required for the current portfolio version.

---

## 31. Technical Trade-Offs

| Area | Current Choice | Trade-Off |
|---|---|---|
| Local warehouse | SQLite | Simple and cheap, but not distributed |
| API auth | API keys | Easy to implement, less advanced than OAuth |
| Orchestration | ADF demo pipeline | Shows Azure orchestration, but not every local pipeline step is cloud-orchestrated |
| Deployment | Manual Docker push | Clear and reliable, but not full CD |
| Monitoring | Availability test | Good basic uptime monitoring, but not full observability |
| Dashboard | Deferred Power BI | Keeps engineering complete before visualization |

These trade-offs are intentional for a first cloud data engineering portfolio project.

---

## 32. Final Technical Architecture Outcome

The final architecture shows a complete technical path from raw data to deployed and monitored cloud API.

It demonstrates:

- How data is ingested
- How data is validated
- How analytical models are built
- How operational anomalies are generated
- How curated data is moved to Azure SQL
- How a FastAPI backend serves the data
- How the API is secured
- How the API is containerized and deployed
- How secrets are managed
- How availability is monitored
- How each major layer is verified

This makes the project technically complete before moving into portfolio packaging and dashboard presentation.