# Data Governance

## Project Name

E-Commerce Retail Intelligence Platform with Operational Anomaly Detection and AI-Ready Business Insights

## Purpose

This document explains how data is managed, validated, documented, protected, deployed, monitored, and verified in this project.

The project uses the Olist Brazilian E-Commerce dataset to simulate a cloud data engineering and analytics engineering platform. The goal is to create trusted business data for reporting, operational anomaly detection, secured API access, and AI-ready business insights.

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

The project does not store real customer names, emails, phone numbers, payment card numbers, or personal addresses.

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

### Transformation and Warehouse Quality Controls

The transformation layer applies controlled staging, warehouse modelling, and dbt validation.

Quality controls include:

- Consistent staging table structure
- Fact and dimension modelling
- Primary key and relationship checks
- Not-null checks on important fields
- Accepted value checks where applicable
- KPI view validation
- Operational anomaly output validation

---

## 5. API Access Governance

The FastAPI backend uses JWT Bearer authentication with role-based access control.

Users authenticate through:

```text
POST /auth/login
```

The login endpoint returns a signed JWT access token. Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

The API supports three demo roles:

| Role | Access Level |
|---|---|
| `admin` | Full access to executive, operations, insights, and admin-level endpoints |
| `analyst` | Access to executive, operations, and insight endpoints |
| `viewer` | Limited summary-level read access |

The public root, health, Swagger, OpenAPI, and login endpoints remain accessible without JWT authentication so that the API can be discovered, monitored, and tested.

### Authentication Endpoints

| Endpoint | Method | Governance Purpose |
|---|---|---|
| `/auth/login` | POST | Authenticates a demo user and returns a JWT access token |
| `/auth/me` | GET | Returns the authenticated user's username and role |

### Role Access Governance

| Endpoint Group | Admin | Analyst | Viewer |
|---|---:|---:|---:|
| Public root and health endpoints | Yes | Yes | Yes |
| Authentication login endpoint | Yes | Yes | Yes |
| Executive summary endpoints | Yes | Yes | Yes |
| Detailed executive endpoints | Yes | Yes | No |
| Operations endpoints | Yes | Yes | No |
| AI-ready summary insight endpoint | Yes | Yes | Yes |
| Detailed AI-ready insight endpoints | Yes | Yes | No |
| LLM context endpoint | Yes | No | No |

JWT signing secrets and demo user credentials are stored in local `.env` for local development and in Azure Key Vault for the deployed Azure App Service.

The real `.env` file is excluded from Git and must not be committed.

---

## 6. API Monitoring and Error Governance

The FastAPI backend includes request logging, error logging, and health check endpoints.

API logs are stored locally in:

```text
logs/api.log
```

The `/health/` endpoint checks API availability and database connectivity.

The `/health/status` endpoint checks whether important warehouse, KPI, operational, and AI-ready source objects are available.

The API uses centralised error handling so unexpected errors are logged while internal stack traces are not exposed to API users.

In Azure, health and availability signals are monitored using Application Insights and Azure Monitor.

---

## 7. Automated Testing Governance

The project includes automated tests to improve reliability and reduce the risk of silent failures.

The test suite is organised into unit, API, and integration tests.

### Test Categories

| Test Category | Purpose |
|---|---|
| Unit tests | Validate individual components such as database helpers and AI-ready insight generation |
| API tests | Validate FastAPI endpoints, JWT authentication, RBAC access rules, and response structure |
| Integration tests | Validate that important generated pipeline outputs exist |
| Cloud verification scripts | Validate Azure Blob, Azure SQL, ADF, App Service, Key Vault, monitoring, and deployment setup |

### Tested Areas

The automated tests validate:

- Database helper behaviour
- Important warehouse, KPI, and operational database objects
- Public health endpoints
- Protected API endpoints
- JWT login and token validation
- Role-based access control
- AI-ready business insight endpoints
- LLM context generation
- Important pipeline output files
- Docker setup
- CI setup

### Test Execution

The test suite can be executed using:

```powershell
python -m pytest
```

Live Azure SQL tests are skipped by default during normal local pytest runs and can be enabled explicitly when Azure SQL is online.

---

## 8. Docker and Deployment Governance

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

In the cloud version, the database is not copied into the application image.

Instead, the deployed API connects to Azure SQL Database.

This keeps the application layer and data storage layer separated.

### Container Access Governance

The containerised API keeps the same governance controls as the local Python version:

- JWT Bearer authentication remains active
- Role-based access control remains active
- Health checks remain available
- Logging remains enabled
- Error handling remains enabled
- AI-ready insight endpoints remain protected by role

### Local vs Cloud Governance

| Area | Local Docker Version | Azure Version |
|---|---|---|
| Database | SQLite file mounted into container at runtime | Azure SQL Database |
| Secrets | Local `.env` file | Azure Key Vault references |
| Authentication | JWT Bearer authentication | JWT Bearer authentication |
| Hosting | Docker Desktop | Azure App Service for Containers |
| Monitoring | Local logs | Application Insights and Azure Monitor |
| Deployment | Manual Docker commands | GitHub Actions CI/CD |
| Runtime environment | Local Docker image | Cloud-hosted Linux container |

### Governance Outcome

The Docker layer shows that the API can be packaged, tested, and executed in a controlled runtime environment without embedding large local data files or secrets into the application image.

---

## 9. CI/CD Governance

The project includes GitHub Actions CI/CD governance to make validation and deployment more controlled and repeatable.

CI/CD governance ensures that the application is not deployed only through manual local commands. Instead, code changes pushed to GitHub trigger automated validation and deployment workflows.

### CI/CD Governance Flow

```text
Code pushed to GitHub
        ↓
CI pipeline validates project
        ↓
CD pipeline builds Docker image
        ↓
Image pushed to Azure Container Registry
        ↓
Azure App Service updated
        ↓
Deployment health check verifies /health/
```

### CI Controls

| Control | Purpose |
|---|---|
| Dependency installation | Confirms the project can install in a clean environment |
| Python syntax validation | Confirms source and script files compile |
| Import validation | Confirms key application modules can be imported |
| Docker setup verification | Confirms Docker-related files and configuration exist |
| CI setup verification | Confirms CI configuration is present and valid |
| Docker image build | Confirms the API image can be built successfully |
| Database tracking check | Prevents the large local SQLite database from being committed |

### CD Controls

| Control | Purpose |
|---|---|
| Azure service principal | Allows GitHub Actions to authenticate to Azure securely |
| GitHub repository secrets | Stores deployment values outside source code |
| Docker image tagging | Tags images as both `latest` and Git commit SHA |
| ACR image push | Publishes deployable images to Azure Container Registry |
| App Service managed identity | Allows secure Azure-side identity management |
| AcrPull role check | Confirms the App Service can pull images from ACR |
| Managed identity ACR pull setting | Avoids storing ACR username/password credentials |
| App Service restart | Applies the new image deployment |
| `/health/` verification | Confirms the deployed API is running and connected to Azure SQL |

### Secret Governance in CI/CD

The CD workflow uses GitHub Actions secrets for deployment configuration.

| Secret | Purpose |
|---|---|
| `AZURE_CREDENTIALS` | Azure service principal credentials |
| `ACR_LOGIN_SERVER` | Azure Container Registry login server |
| `AZURE_WEBAPP_NAME` | Azure App Service name |
| `AZURE_RESOURCE_GROUP` | Azure resource group |
| `AZURE_APP_BASE_URL` | Deployed API base URL |

The workflow does not commit these values to Git.

Application runtime secrets such as SQL credentials, JWT signing secrets, and demo JWT user credentials remain stored in Azure Key Vault.

---

## 10. Azure SQL Database Governance

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
| API serving layer | Executive, operations, and insights serving objects |

Raw CSV files and the local SQLite database are not uploaded into Azure SQL directly as unmanaged raw artifacts.

### Access and Security Governance

Azure SQL connection values are stored in local `.env` for local development and in Azure Key Vault for the Azure deployment.

The `.env` file is ignored by Git and must not be committed to GitHub.

The safe placeholder variables are documented in `.env.example`.

### Firewall Governance

Azure SQL firewall access should be limited to required client IP addresses and Azure service access required by the deployment.

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

Free offer behaviour may pause the database after the monthly allowance is reached. This is acceptable for cost control, but live cloud verification and CD health checks require Azure SQL to be online.

---

## 11. Azure Data Factory Governance

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
- Additional Azure Key Vault integration
- Additional monitoring and alerting

---

## 12. Azure App Service Governance

The deployed FastAPI backend introduces a cloud application layer that requires governance around secrets, access control, deployment, and operational reliability.

### Runtime Configuration Governance

The deployed API is configured using Azure App Service environment variables.

Secrets and runtime configuration values are not committed to GitHub.

Sensitive values include:

- Azure SQL username
- Azure SQL password
- JWT signing secret
- Demo JWT user passwords
- Connection strings

The `.env.example` file contains placeholders only and is safe for documentation.

The real `.env` file is excluded from version control.

### API Access Control

The API uses JWT Bearer authentication with role-based access control.

Protected endpoints require the following header:

```text
Authorization: Bearer <access_token>
```

Users obtain the access token through:

```text
POST /auth/login
```

This prevents unauthenticated access to business and operational data endpoints.

### Container Registry Access

Azure App Service pulls the Docker image from Azure Container Registry using managed identity.

The Web App has the following permission on the registry:

```text
AcrPull
```

This is preferred over enabling ACR admin credentials because it avoids registry username/password usage.

### Database Access

The deployed API connects to Azure SQL Database using Key Vault-backed environment variables.

Current implementation:

```text
App Service Key Vault references
        ↓
Environment variables
        ↓
SQLAlchemy / pyodbc
        ↓
Azure SQL Database
```

### Deployment Governance

The deployment uses a controlled image-based release process:

```text
GitHub Actions CD
        ↓
Build Docker image
        ↓
Push image to Azure Container Registry
        ↓
Azure App Service pulls approved image tag
        ↓
Verify deployed /health/ endpoint
```

The CD pipeline pushes both:

```text
latest
<github.sha>
```

The commit-SHA tag improves traceability.

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

## 13. Azure Key Vault Governance

Azure Key Vault is used to centralise and protect sensitive runtime values for the deployed API.

### Governed Secrets

The following secret categories are governed through Key Vault:

| Secret Category | Examples |
|---|---|
| Database connection values | SQL server, database name, username, password |
| JWT authentication values | JWT signing secret and demo user credentials |

Actual values are not documented and are not committed to source control.

### JWT Secrets

| Key Vault Secret | App Service Setting | Purpose |
|---|---|---|
| `jwt-secret-key` | `JWT_SECRET_KEY` | Signs JWT access tokens |
| `jwt-admin-username` | `JWT_ADMIN_USERNAME` | Demo admin username |
| `jwt-admin-password` | `JWT_ADMIN_PASSWORD` | Demo admin password |
| `jwt-analyst-username` | `JWT_ANALYST_USERNAME` | Demo analyst username |
| `jwt-analyst-password` | `JWT_ANALYST_PASSWORD` | Demo analyst password |
| `jwt-viewer-username` | `JWT_VIEWER_USERNAME` | Demo viewer username |
| `jwt-viewer-password` | `JWT_VIEWER_PASSWORD` | Demo viewer password |

Non-sensitive JWT settings can remain as plain App Service settings:

| App Service Setting | Value |
|---|---|
| `JWT_ALGORITHM` | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |

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

### Runtime Secret Injection

App Service uses Key Vault references in application settings.

Example pattern:

```text
@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-secret-key)
```

At runtime, App Service resolves this reference and exposes the resolved value as an environment variable.

The FastAPI app does not need to directly call Key Vault.

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

## 14. Monitoring and Operational Governance

Azure monitoring is used to provide operational visibility for the deployed API.

### Monitoring Controls

| Control | Purpose |
|---|---|
| App Service logging | Captures application and container log activity |
| Log Stream | Supports live troubleshooting |
| Application Insights | Tracks API availability |
| Availability test | Verifies `/health/` endpoint from external locations |
| Alert rule | Detects availability failures |

### Availability Governance

The deployed API is monitored through a Standard availability test.

| Field | Value |
|---|---|
| Test name | `fastapi-health-check` |
| Endpoint | `/health/` |
| Expected status | HTTP 200 |
| Frequency | 5 minutes |
| Failure rule | Failed locations >= 2 |

The `/health/` endpoint remains public because it is used for monitoring and deployment smoke tests.

### Cost Governance

The project uses cost-conscious Azure choices.

Application Insights availability testing is used as the primary monitoring approach. Built-in App Service Health Check is optional and depends on the active App Service plan.

The App Service plan may be scaled up temporarily when needed for reliable deployment or troubleshooting, then reviewed for cost control.

### Logging Governance

Logs are used for troubleshooting and operational validation.

The project avoids logging sensitive values such as:

- SQL passwords
- JWT signing secrets
- JWT user passwords
- Key Vault secret values
- Connection strings

Secrets remain stored in Azure Key Vault and are not written to logs or documentation.

### Verification Evidence

Monitoring setup is verified through:

```powershell
python scripts\verify_azure_monitoring_setup.py
```

The verification report is saved to:

```text
data/processed/azure_monitoring_setup_verification_report.csv
```

This report documents both manual Azure monitoring setup checks and automated deployed endpoint checks.

---

## 15. Final Technical Governance Summary

The final platform includes governance controls across data quality, security, deployment, monitoring, and documentation.

This governance layer helps show that the project is not only a data pipeline, but a controlled cloud data platform.

### Governance Across the Final Architecture

| Area | Governance Control | Purpose |
|---|---|---|
| Raw data | Raw files preserved separately | Keeps original source data traceable |
| Data quality | Validation scripts and reports | Makes data issues visible before analytics |
| Transformations | dbt models and tests | Provides structured and testable analytics engineering logic |
| Warehouse | Facts, dimensions, and curated views | Separates raw data from business-ready outputs |
| Operational intelligence | Anomaly rules and alert tables | Converts operational issues into structured outputs |
| API access | JWT authentication and RBAC | Restricts access by user role |
| Secret management | Azure Key Vault | Keeps sensitive values out of source code and plain settings |
| Container deployment | Docker, ACR, and App Service | Provides repeatable API deployment |
| CI/CD | GitHub Actions | Automates validation and deployment |
| Monitoring | App Service Logs and Application Insights | Provides availability and troubleshooting visibility |
| Verification | Scripts and CSV reports | Creates evidence that each layer works |
| Documentation | Architecture and setup docs | Makes the system explainable and auditable |

### Data Governance Flow

```text
Raw source files
    ↓
Raw SQLite tables
    ↓
Data quality checks
    ↓
Staging models
    ↓
Warehouse facts and dimensions
    ↓
KPI and anomaly outputs
    ↓
API serving layer
```

Business users and API consumers do not work directly from raw data. They consume curated and documented outputs.

### Security Governance Flow

```text
Secrets
    ↓
Azure Key Vault
    ↓
App Service Key Vault references
    ↓
Environment variables
    ↓
FastAPI runtime
    ↓
JWT authentication and RBAC authorization
```

Security controls include:

- `.env` excluded from Git
- No secrets stored in Docker image
- SQL credentials stored in Key Vault
- JWT signing secret stored in Key Vault
- Demo JWT user credentials stored in Key Vault
- App Service managed identity used for Key Vault access
- App Service managed identity used for ACR image pull
- Protected API routes require `Authorization: Bearer <access_token>`
- RBAC limits endpoint access by role

### Monitoring Governance Flow

```text
Azure App Service
    ↓
Application logs and Log Stream

Application Insights
    ↓
Availability test on /health/
    ↓
Automatic alert rule
```

Monitoring controls include:

- App Service logging enabled
- Log Stream verified
- Application Insights resource created
- Availability test configured for `/health/`
- Automatic alert rule created for failed locations
- Monitoring verification report generated

### Verification Governance

Every major platform layer has a verification step.

| Layer | Verification Evidence |
|---|---|
| Automated tests | `data/processed/automated_test_run_summary.csv` |
| Docker | `scripts/verify_docker_setup.py` |
| Azure Blob Storage | `data/processed/azure_blob_upload_report.csv` and Blob verification report |
| Azure SQL Database | `data/processed/azure_sql_setup_verification_report.csv` |
| Azure Data Factory | `data/processed/adf_pipeline_output_verification_report.csv` |
| Azure App Service | `data/processed/azure_app_deployment_verification_report.csv` |
| Azure Key Vault | `data/processed/key_vault_setup_verification_report.csv` |
| Azure Monitoring | `data/processed/azure_monitoring_setup_verification_report.csv` |
| CI/CD | GitHub Actions workflow runs and screenshots |
| JWT Authentication | `tests/api/test_api_jwt_auth.py` and API RBAC tests |

### Final Documentation Governance

The final technical documentation is split by purpose.

| Document | Governance Purpose |
|---|---|
| `docs/project_showcase.md` | Provides screenshot-backed portfolio walkthrough |
| `docs/final_architecture.md` | Provides final architecture summary |
| `docs/technical_architecture.md` | Documents technical architecture and runtime design |
| `docs/system_flow.md` | Explains end-to-end data, API, deployment, security, and monitoring flow |
| `docs/architecture.md` | Preserves detailed architecture notes |
| `docs/setup_guide.md` | Explains how to configure and verify the system |
| `docs/data_dictionary.md` | Documents tables, outputs, reports, and technical artifacts |
| `docs/azure_ci_cd.md` | Documents CI/CD deployment automation |

### Final Governance Outcome

At the end of the technical build, the project includes governance across:

```text
Data quality
Transformation testing
Warehouse modelling
JWT API access control
Secret management
Cloud deployment
CI/CD automation
Monitoring
Verification evidence
Documentation
```

This improves the project from a simple analytics build into a more complete cloud data engineering platform.
