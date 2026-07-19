# Data Governance

## Project Name

E-Commerce Retail Intelligence Platform with Operational Anomaly Detection and AI Business Insights

## Purpose

This document explains how data is managed, validated, documented, and protected in this project.

The project uses the Olist Brazilian E-Commerce dataset to simulate a real e-commerce data platform. The goal is to create trusted business data for reporting, operational anomaly detection, API access, and AI-generated business insights.

---

## 1. Data Sources

The main source is the Olist Brazilian E-Commerce Public Dataset.

Source files include:

| Source File | Description |
|---|---|
| `olist_customers_dataset.csv` | Customer and customer location data |
| `olist_geolocation_dataset.csv` | Brazilian geolocation reference data |
| `olist_order_items_dataset.csv` | Order item, product, seller, price, and freight data |
| `olist_order_payments_dataset.csv` | Payment method and payment value data |
| `olist_order_reviews_dataset.csv` | Customer review data |
| `olist_orders_dataset.csv` | Order lifecycle and delivery timestamp data |
| `olist_products_dataset.csv` | Product category and product attributes |
| `olist_sellers_dataset.csv` | Seller location data |
| `product_category_name_translation.csv` | Product category translation mapping |

---

## 2. Data Ownership Assumption

In a real organisation, ownership would be split as follows:

| Data Area | Example Owner |
|---|---|
| Orders | Operations team |
| Payments | Finance team |
| Sellers | Marketplace operations team |
| Products | Product catalogue team |
| Reviews | Customer experience team |
| Delivery | Logistics team |
| Reporting layer | Data/BI team |
| AI insights layer | Data/AI team |

For this portfolio project, all data ownership is simulated and managed inside the project repository.

---

## 3. Data Classification

The dataset is anonymised and does not contain direct personal identifiers such as names, phone numbers, emails, or addresses.

| Data Type | Classification |
|---|---|
| Customer IDs | Pseudonymous identifier |
| Seller IDs | Pseudonymous identifier |
| Order IDs | Transactional identifier |
| Product IDs | Product identifier |
| Review scores | Business/customer satisfaction data |
| Location state/city | Aggregated geography |
| Payment values | Business transaction data |

The project does not store real customer names, emails, phone numbers, or payment card details.

---

## 4. Data Quality Controls

The project applies data quality checks at multiple stages.

### Raw Data Quality Checks

Raw quality checks validate:

- Missing primary keys
- Duplicate identifiers
- Invalid foreign key relationships
- Negative price values
- Negative freight values
- Negative payment values
- Invalid delivery dates
- Missing delivery dates for delivered orders
- Review scores outside the valid range

Output:

```text
data/processed/raw_data_quality_results.csv
```


## API Access Governance

The FastAPI backend includes simple API-key based authentication and role-based access control.

| Role | Access Level |
|---|---|
| Admin | Full API access |
| Analyst | Executive and operational read access |
| Viewer | Limited executive read access |

Protected endpoints require the `X-API-Key` request header.

Viewer users can access only high-level executive endpoints. Analyst users can access executive and operational read endpoints. Admin users can access all current endpoints.

The local version uses demo API keys for portfolio demonstration. In the Azure version, secrets will be stored in Azure Key Vault and access will be managed using a stronger production authentication mechanism.

## API Monitoring and Error Governance

The FastAPI backend includes request logging, error logging, and health check endpoints.

API logs are stored in:

`logs/api.log`

The `/health/` endpoint checks database connectivity.

The `/health/status` endpoint checks whether important warehouse, KPI, operational, and AI-ready source objects are available.

The API uses centralised error handling so unexpected errors are logged but internal stack traces are not exposed to API users.

In the Azure version, these logs and health signals will be connected to Azure Monitor.


---

## Automated Testing Governance

The project includes automated tests to improve reliability and reduce the risk of silent failures.

The test suite is organised into unit, API, and integration tests.

### Test Categories

| Test Category | Purpose |
|---|---|
| Unit tests | Validate individual components such as database helpers and AI-ready insight generation |
| API tests | Validate FastAPI endpoints, authentication, RBAC access rules, and response structure |
| Integration tests | Validate that important generated pipeline outputs exist |

### Tested Areas

The automated tests validate:

- Database connectivity
- Important warehouse, KPI, and operational database objects
- Public health endpoints
- Protected API endpoints
- API-key authentication
- Role-based access control
- AI-ready business insight endpoints
- LLM context generation
- Important pipeline output files

### Test Execution

The test suite can be executed using:

```powershell
pytest tests -v
```


## Docker and Deployment Governance

The project includes Docker containerisation for the FastAPI backend.

Docker improves deployment governance by making the API runtime environment more reproducible, portable, and easier to test before cloud deployment.

### Governance Benefits

Docker supports the project by providing:

- Reproducible API execution
- Consistent dependency installation
- Cleaner separation between development and runtime environments
- Easier testing before deployment
- Better preparation for CI/CD workflows
- Better preparation for Azure deployment

### Local Container Design

The local Docker version uses the SQLite database file:

```text
retail_intelligence.db
```

The database is not copied into the Docker image.

Instead, it is mounted into the container at runtime.

This keeps the image smaller and separates application code from runtime data.

### Production-Style Governance Note

In a production-style cloud version, the database should not be copied into the application image.

Instead, the API should connect to a managed database service such as Azure SQL Database.

This keeps the application layer and data storage layer separated.

### Security Notes

The local Docker version uses demo API keys for testing:

| Role | Demo Key |
|---|---|
| Admin | `admin-demo-key` |
| Analyst | `analyst-demo-key` |
| Viewer | `viewer-demo-key` |

These keys are suitable only for local demonstration.

In the Azure version, secrets should be stored in Azure Key Vault instead of being hardcoded or stored directly in the application image.

### Access Governance

The same API access rules apply inside the Docker container:

| Area | Governance Rule |
|---|---|
| Public endpoints | Health and root endpoints remain publicly accessible |
| Protected endpoints | Require `X-API-Key` authentication |
| Admin endpoints | Require admin-level access |
| Analyst endpoints | Available to analyst and admin roles |
| Viewer endpoints | Limited to selected read-only executive and insight endpoints |

### Deployment Governance

The containerised API keeps the same governance controls as the local Python version:

- API-key authentication remains active
- Role-based access control remains active
- Health checks remain available
- Logging remains enabled
- Error handling remains enabled
- AI-ready insight endpoints remain protected by role

### Local vs Cloud Governance

| Area | Local Docker Version | Future Azure Version |
|---|---|---|
| Database | SQLite file mounted into container at runtime | Azure SQL Database |
| Secrets | Demo API keys | Azure Key Vault |
| Hosting | Docker Desktop | Azure App Service or container hosting |
| Monitoring | Local logs | Azure Monitor |
| Deployment | Manual Docker commands | CI/CD pipeline |
| Runtime environment | Local Docker image | Cloud-hosted container or app service |

### Governance Outcome

This Docker phase prepares the project for future CI/CD and Azure deployment phases.

It shows that the API can be packaged, tested, and executed in a controlled runtime environment without embedding large local data files into the application image.


## CI Governance

The project includes a GitHub Actions CI pipeline to improve reliability and reduce the risk of broken code being pushed or merged.

### CI Governance Controls

| Control | Purpose |
|---|---|
| Automated workflow | Runs validation checks automatically on GitHub |
| Database tracking check | Prevents the large local SQLite database from being committed |
| Dependency installation | Confirms project dependencies can be installed |
| Syntax validation | Confirms Python files can compile successfully |
| Import validation | Confirms core application modules can be imported |
| Docker setup verification | Confirms Docker setup and documentation are present |
| CI setup verification | Confirms CI workflow and documentation are present |
| Docker build check | Confirms the API container image can be built |
| Pull request validation | Allows changes to be checked before merging |
| Manual workflow dispatch | Allows the workflow to be triggered manually |

### CI Pipeline Scope

The CI pipeline runs database-independent checks:

```text
python -m compileall src scripts
python scripts/verify_docker_setup.py
python scripts/verify_ci_setup.py
docker build -t ecommerce-retail-api .
```

The pipeline also checks that the large local SQLite database is not tracked by Git.

### Local Database Governance

The local SQLite database file:

```text
retail_intelligence.db
```

is a generated local artifact and should not be committed to GitHub.

This keeps the repository lightweight and avoids storing large generated data files in source control.

### Local Testing vs CI Testing

| Area | Local Testing | GitHub Actions CI |
|---|---|---|
| Database-backed API tests | Yes | Not yet |
| RBAC endpoint tests | Yes | Not yet |
| Pipeline output tests | Yes | Not yet |
| Python syntax validation | Yes | Yes |
| Core import validation | Yes | Yes |
| Docker setup verification | Yes | Yes |
| Docker image build | Yes | Yes |

Full database/API tests can be added to CI later after Azure SQL Database or a smaller CI test database is available.

### Current CI/CD Boundary

This phase implements Continuous Integration.

It does not automatically deploy the application to Azure yet.

Continuous Deployment will be implemented later after:

- Azure SQL Database
- Azure Key Vault
- Azure App hosting
- Azure Monitor

are completed.


## Azure SQL Database Governance

Azure SQL Database is used as the cloud serving database for curated analytical outputs.

This layer introduces cloud database governance for structured serving data.

### Data Governance Role

Azure SQL stores curated outputs rather than raw files.

Raw source files remain in Azure Blob Storage, while cleaned and modelled analytical tables are loaded into Azure SQL.

This separation supports a clear data architecture:

```text
Raw data → Azure Blob Storage
Curated serving data → Azure SQL Database
```

### Loaded Data Scope

The Azure SQL migration focuses on curated, business-ready objects:

| Data Area | Examples |
|---|---|
| Dimensions | Customer, product, seller, and date dimensions |
| Facts | Sales, delivery, payment, and review facts |
| Operational metrics | Daily, seller, and category operational metrics |
| Anomaly detection | Operational anomaly rules and alerts |
| Event pipeline | Event log and processed event records |

Raw CSV files and the local SQLite database are not uploaded into Azure SQL directly as unmanaged raw artifacts.

### Access and Security Governance

Azure SQL credentials are stored only in the local `.env` file.

The `.env` file is ignored by Git and must not be committed to GitHub.

The safe placeholder variables are documented in `.env.example`.

This phase uses SQL authentication for local development and portfolio demonstration.

In a later phase, secrets will be managed using Azure Key Vault.

### Firewall Governance

Azure SQL firewall access is configured to allow the local development machine to connect.

Firewall access should be limited to required client IP addresses.

Broad public access should be avoided.

### Migration Governance

The migration script creates a structured report:

```text
data/processed/azure_sql_migration_report.csv
```

This report records:

- Object name
- Migration status
- Loaded row count
- Start time
- Finish time
- Error details, if any

### Verification Governance

The verification script creates:

```text
data/processed/azure_sql_setup_verification_report.csv
```

This report checks:

- Required local files
- Required environment variable documentation
- Required Python dependencies
- Expected Azure SQL tables
- Loaded table row counts

### Cost Governance

The Azure SQL Database should use a low-cost or free-tier configuration where available.

Free offer behavior should be configured to pause or stop usage when the monthly free limit is reached.

This helps avoid unexpected charges during portfolio development.

### Current Limitation

The FastAPI backend still uses local SQLite at this stage.

Azure SQL is currently used as the cloud serving database and migration target.

A later phase can update the API configuration to use Azure SQL as a live backend database source.

### Governance Outcome

This phase adds cloud database governance by separating raw landing-zone storage from curated serving-layer storage.

It also introduces controlled credentials, firewall configuration, migration reporting, and verification reporting.


## Azure Data Factory Governance

Azure Data Factory is used as the cloud orchestration layer between Azure Blob Storage and Azure SQL Database.

### Governance Role

ADF controls the movement of raw data from the cloud landing zone into a structured Azure SQL staging table.

### Pipeline Governance

The implemented pipeline copies one raw source file:

```text
raw/olist/olist_orders_dataset.csv
```

into:

```text
dbo.adf_stg_orders_raw
```

The sink table is truncated before each pipeline run to avoid duplicate records.

### Separation of Concerns

The ADF staging table is separate from the curated warehouse and operational tables.

This ensures raw ingestion testing does not overwrite curated analytical outputs.

### Current Scope

This phase proves cloud orchestration with one representative raw file.

Future improvements can include:

- Parameterised datasets
- Metadata-driven ingestion
- Scheduled triggers
- Multiple file ingestion
- Azure Key Vault integration
- Monitoring and alerting


## Azure App Service Governance

The deployed FastAPI backend introduces a cloud application layer that requires governance around secrets, access control, deployment, and operational reliability.

### Runtime Configuration Governance

The deployed API is configured using Azure App Service environment variables.

Secrets and runtime configuration values are not committed to GitHub.

Sensitive values include:

- Azure SQL username
- Azure SQL password
- API keys
- Connection strings

The `.env.example` file contains placeholders only and is safe for documentation.

The real `.env` file is excluded from version control.

---

### API Access Control

The API uses API key based role-based access control.

| Role | Access Level |
|---|---|
| Admin | Full API access |
| Analyst | Business, operations, and insights access |
| Viewer | Limited read-only access |

Protected endpoints require the following header:

```text
X-API-Key
```

This prevents unauthenticated access to business and operational data endpoints.

---

### Container Registry Access

Azure App Service pulls the Docker image from Azure Container Registry using managed identity.

The Web App has the following permission on the registry:

```text
AcrPull
```

This is preferred over enabling ACR admin credentials because it avoids registry username/password usage.

---

### Database Access

The deployed API connects to Azure SQL Database using environment variables.

Current implementation:

```text
App Service environment variables → SQLAlchemy / pyodbc → Azure SQL Database
```

Future improvement:

```text
App Service managed identity → Azure Key Vault → Azure SQL secrets
```

Azure Key Vault will be added in a later phase to centralize secret management.

---

### Deployment Governance

The deployment uses a controlled image-based release process:

```text
Build Docker image locally
        ↓
Push image to Azure Container Registry
        ↓
Azure App Service pulls approved image tag
        ↓
Verify deployed endpoints
```

This makes deployments repeatable and auditable.

The deployed image tag used in this phase is:

```text
latest
```

For production-grade release governance, versioned tags such as `v1.0.0` would be preferable.

---

### Verification Governance

The deployed API is validated using:

```powershell
python scripts\verify_azure_app_deployment.py
```

The verification produces a CSV report:

```text
data/processed/azure_app_deployment_verification_report.csv
```

This report provides evidence that the deployed API endpoints are available and returning successful responses.

---

### Current Limitations

Current limitations are intentionally documented for transparency:

- API keys are stored as App Service environment variables.
- Azure SQL credentials are stored as App Service environment variables.
- The deployed container uses the `latest` image tag.
- Full Azure Monitor alerting is not yet configured.
- Key Vault integration is not yet implemented.

These limitations will be addressed in later phases through Azure Key Vault, monitoring, and final deployment hardening.


## Azure Key Vault Governance

Azure Key Vault is used to centralize and protect sensitive runtime values for the deployed API.

### Governed Secrets

The following secret categories are governed through Key Vault:

| Secret Category | Examples |
|---|---|
| Database connection values | SQL server, database name, username, password |
| API access keys | Admin, Analyst, Viewer API keys |

Actual values are not documented and are not committed to source control.

---

### Access Control Model

The Key Vault uses Azure role-based access control.

| Principal | Role | Purpose |
|---|---|---|
| Developer Azure user | `Key Vault Secrets Officer` | Create and manage secrets |
| App Service managed identity | `Key Vault Secrets User` | Read secrets at runtime |

This follows least-privilege principles:

- The developer can manage secrets.
- The application can only read secrets.
- The application does not need vault administration rights.

---

### Secret Storage Policy

Secrets must not be stored in:

- GitHub source code
- Docker images
- Documentation files
- README files
- Screenshots
- `.env.example`

The `.env.example` file contains placeholders only.

The real `.env` file is excluded from Git tracking.

---

### Runtime Secret Injection

App Service uses Key Vault references in application settings.

Example pattern:

```text
@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-password)
```

At runtime, App Service resolves this reference and exposes the resolved value as an environment variable.

The FastAPI app does not need to directly call Key Vault.

---

### Verification Evidence

The Key Vault configuration is verified using:

```powershell
python scripts\verify_key_vault_setup.py
```

The verification report is stored at:

```text
data/processed/key_vault_setup_verification_report.csv
```

This report confirms that the deployed API still works after secret values are moved from App Service plain settings to Key Vault references.

---

### Current Security Position

Implemented controls:

- Key Vault stores SQL credentials and API keys.
- App Service uses managed identity for secret access.
- App Service also uses managed identity for ACR image pull.
- API endpoints are protected with role-based API keys.
- Real secrets are excluded from GitHub.
- `.env.example` uses placeholders only.

Remaining future improvements:

- Rotate API keys periodically.
- Use versioned Docker image tags instead of `latest`.
- Add Azure Monitor alerts.
- Consider Entra ID authentication for production-grade API security.
- Consider managed identity authentication to Azure SQL in a future advanced phase.