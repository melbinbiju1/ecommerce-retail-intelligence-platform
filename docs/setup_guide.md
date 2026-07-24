# Setup Guide

## Purpose

This setup guide explains how to run and validate the **E-Commerce Retail Intelligence Platform** locally.

The guide covers:

- Python environment setup
- Dependency installation
- Automated tests
- Docker execution
- GitHub Actions CI-equivalent checks

## Final Technical Documentation

After completing the cloud deployment, security, and monitoring phases, the project includes final technical documentation to explain the complete system architecture.

Use these documents to understand the final implemented platform:

| Document | Purpose |
|---|---|
| `docs/final_architecture.md` | Final end-to-end architecture summary |
| `docs/technical_architecture.md` | Detailed technical design decisions, runtime modes, trade-offs, security, deployment, and monitoring architecture |
| `docs/system_flow.md` | Step-by-step system flow covering data, API, deployment, secret management, and monitoring |
| `docs/architecture.md` | Detailed working architecture document updated throughout the project |

Recommended reading order:

```text
1. docs/final_architecture.md
2. docs/system_flow.md
3. docs/technical_architecture.md
4. docs/architecture.md
```

These documents explain how the platform moves from raw Olist CSV files to a secured and monitored Azure-hosted FastAPI API.

## Project Prerequisites

Install the following tools before running the project:

| Tool | Purpose |
|---|---|
| Python 3.10 | Runs the data pipeline, FastAPI backend, tests, and verification scripts |
| Git | Tracks source code and pushes changes to GitHub |
| Docker Desktop | Builds and runs the FastAPI backend inside a container |
| Power BI Desktop | Builds the final reporting dashboard |
| VS Code | Recommended code editor |

## Python Environment Setup

Create a virtual environment from the project root:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Environment Variables

The project uses local environment variables for database settings and JWT authentication.

Create a local `.env` file from `.env.example` if needed:

```powershell
copy .env.example .env
```

The `.env` file should contain runtime settings for local development, including:

```env
APP_ENV=local

JWT_SECRET_KEY=your-generated-jwt-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

JWT_ADMIN_USERNAME=admin
JWT_ADMIN_PASSWORD=your-admin-password

JWT_ANALYST_USERNAME=analyst
JWT_ANALYST_PASSWORD=your-analyst-password

JWT_VIEWER_USERNAME=viewer
JWT_VIEWER_PASSWORD=your-viewer-password
```

Generate strong local JWT values with:

```powershell
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(64)); print('JWT_ADMIN_PASSWORD=' + secrets.token_urlsafe(24)); print('JWT_ANALYST_PASSWORD=' + secrets.token_urlsafe(24)); print('JWT_VIEWER_PASSWORD=' + secrets.token_urlsafe(24))"
```

The API supports three demo JWT users:

| Role | Username | Access Level |
|---|---|---|
| Admin | `admin` | Full API access |
| Analyst | `analyst` | Executive, operational, and insight read access |
| Viewer | `viewer` | Limited summary-level read access |

Do not commit `.env`, JWT secrets, passwords, database credentials, or connection strings to GitHub.

## JWT Authentication Setup

The API uses JWT Bearer authentication with role-based access control.

Authentication flow:

```text
POST /auth/login
        ↓
JWT access token returned
        ↓
Authorization: Bearer <access_token>
        ↓
Protected endpoint access
```

Role access summary:

| Role | Access |
|---|---|
| `admin` | Full access to executive, operations, insights, and admin-level endpoints |
| `analyst` | Executive, operations, and insight access |
| `viewer` | Limited summary-level read access |

Local JWT test:

```powershell
$loginResponse = Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/auth/login" `
  -ContentType "application/x-www-form-urlencoded" `
  -Body "username=viewer&password=<viewer-password>"

$headers = @{
    "Authorization" = "Bearer $($loginResponse.access_token)"
}

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/executive/summary" `
  -Headers $headers
```

The `/health/` endpoint remains public for monitoring and CI/CD smoke testing.


## Local Database

The local project uses a generated SQLite database:

```text
retail_intelligence.db
```

This file is generated locally by the project pipeline.

The database is not committed to GitHub because it is a large generated artifact.

It is ignored using `.gitignore`.

## Run Automated Tests Locally

Run the full local test suite:

```powershell
pytest tests -v
```

Or use the project test runner:

```powershell
python scripts\run_tests.py
```

The test runner creates:

```text
logs/test_run.log
```

and:

```text
data/processed/automated_test_run_summary.csv
```

## Run the FastAPI Backend Locally

Start the FastAPI API without Docker:

```powershell
$env:APP_ENV="local"
uvicorn src.api.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Useful public local API endpoints:

```text
/
```

```text
/health/
```

```text
/health/status
```

JWT authentication endpoints:

```text
/auth/login
```

```text
/auth/me
```

Protected endpoints require JWT Bearer authentication.

Login through Swagger using:

```text
POST /auth/login
```

Then authorize protected requests with:

```text
Authorization: Bearer <access_token>
```

Example local PowerShell test:

```powershell
$loginResponse = Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/auth/login" `
  -ContentType "application/x-www-form-urlencoded" `
  -Body "username=admin&password=<admin-password>"

$headers = @{
    "Authorization" = "Bearer $($loginResponse.access_token)"
}

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/executive/summary" `
  -Headers $headers
```

## Running the API with Docker

The FastAPI backend can also be run inside a Docker container.

This provides a clean and reproducible runtime environment.

### Check Docker

Make sure Docker Desktop is installed and running.

Run:

```powershell
docker version
```

A working setup should show both:

```text
Client
Server
```

The Docker context should use Linux containers.

Example:

```text
Context: desktop-linux
```

### Build the Docker Image

From the project root, run:

```powershell
docker build -t ecommerce-retail-api .
```

This creates a Docker image named:

```text
ecommerce-retail-api
```

### Run the Docker Container with SQLite Mount

The local Docker version does not copy the SQLite database into the image.

Instead, the database is mounted into the container at runtime.

Before running Docker, make sure this file exists in the project root:

```powershell
Get-Item retail_intelligence.db
```

Run the container:

```powershell
docker run --name ecommerce-retail-api-container -p 8000:8000 -v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db ecommerce-retail-api
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### Run the Docker Container in Detached Mode

Detached mode runs the container in the background:

```powershell
docker run -d --name ecommerce-retail-api-container -p 8000:8000 -v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db ecommerce-retail-api
```

Check running containers:

```powershell
docker ps
```

View container logs:

```powershell
docker logs ecommerce-retail-api-container
```

Stop the container:

```powershell
docker stop ecommerce-retail-api-container
```

Remove the container:

```powershell
docker rm ecommerce-retail-api-container
```

## Running CI Checks Locally

Before pushing to GitHub, run the same checks used by the GitHub Actions CI pipeline.

### Validate Python Syntax

```powershell
python -m compileall src scripts
```

### Verify Docker Setup

```powershell
python scripts\verify_docker_setup.py
```

### Verify CI Setup

```powershell
python scripts\verify_ci_setup.py
```

### Build Docker Image

```powershell
docker build -t ecommerce-retail-api .
```

These checks match the main database-independent validations performed in GitHub Actions.

## GitHub Actions CI Workflow

The CI workflow is located at:

```text
.github/workflows/ci.yml
```

The CI pipeline validates:

- The large local SQLite database is not tracked in Git
- Python dependencies can be installed
- Python syntax is valid
- Core Python modules can be imported
- Docker setup is documented and verified
- CI setup is documented and verified
- Docker image can be built

The CI pipeline does not run database-backed API tests yet because the local SQLite database is not committed to GitHub.

Full database-backed CI tests can be added later after Azure SQL Database or a smaller CI test database is available.

## Useful Cleanup Commands

Stop and remove the Docker container:

```powershell
docker stop ecommerce-retail-api-container
docker rm ecommerce-retail-api-container
```

Remove the Docker image:

```powershell
docker rmi ecommerce-retail-api
```

## Detailed Documentation

Additional documentation is available in:

| File | Purpose |
|---|---|
| `README.md` | Main project overview |
| `docker/README.md` | Detailed Docker setup and troubleshooting |
| `docs/architecture.md` | Architecture explanation |
| `docs/data_governance.md` | Governance, quality, security, and CI notes |
| `docs/data_dictionary.md` | Project files, tables, views, and technical artifacts |


## Azure SQL Database Setup

Azure SQL Database is used as the cloud serving database for curated warehouse, KPI, operational, anomaly, and event pipeline outputs.

### Prerequisites

Before running the Azure SQL scripts, make sure:

- Azure SQL Server has been created
- Azure SQL Database has been created
- Your current client IP has been allowed in the Azure SQL firewall
- The local `.env` file contains Azure SQL credentials
- SQL Server ODBC Driver 18 is installed

Check installed ODBC drivers:

```powershell
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"} | Select-Object Name
```

Recommended driver:

```text
ODBC Driver 18 for SQL Server
```

### Environment Variables

Add the following values to your local `.env` file:

```text
AZURE_SQL_SERVER=your-server-name.database.windows.net
AZURE_SQL_DATABASE=sqldb-ecommerce-retail-intelligence
AZURE_SQL_USERNAME=your_sql_admin_username
AZURE_SQL_PASSWORD=your_sql_admin_password
AZURE_SQL_DRIVER=ODBC Driver 18 for SQL Server
```

Do not commit the real `.env` file to GitHub.

### Install Dependencies

Make sure these packages are included in `requirements.txt`:

```text
sqlalchemy
pyodbc
python-dotenv
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

### Test Azure SQL Connection

Run:

```powershell
python scripts\test_azure_sql_connection.py
```

Expected result:

```text
Azure SQL Database connection successful.
```

The connection test report is saved to:

```text
data/processed/azure_sql_connection_test_report.csv
```

### Migrate Curated Data to Azure SQL

Run:

```powershell
python scripts\migrate_curated_data_to_azure_sql.py
```

The migration script loads selected curated objects from the local SQLite database into Azure SQL.

The migration report is saved to:

```text
data/processed/azure_sql_migration_report.csv
```

### Verify Azure SQL Setup

Run:

```powershell
python scripts\verify_azure_sql_setup.py
```

Expected result:

```text
Azure SQL setup verification passed.
```

The verification report is saved to:

```text
data/processed/azure_sql_setup_verification_report.csv
```

### Azure SQL Documentation

Detailed Azure SQL documentation is available in:

```text
docs/azure_sql_database.md
```

## Azure App Service Deployment Setup

This section explains how to deploy the FastAPI backend to Azure App Service as a Docker container.

### Prerequisites

Before deploying the API, complete the following phases:

- Azure Blob Storage setup
- Azure SQL Database setup
- Azure Data Factory setup
- Docker setup
- Azure Container Registry setup
- API serving views migrated to Azure SQL

Required local tools:

- Docker Desktop
- Azure CLI
- Git
- Python virtual environment

---

### 1. Build the Docker Image

From the project root, run:

```powershell
docker build -t ecommerce-retail-api .
```

---

### 2. Log in to Azure Container Registry

```powershell
az acr login --name acrecommerceretailmelbin
```

If `az` is not available in the current terminal, use the full Azure CLI path:

```powershell
& "C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd" acr login --name acrecommerceretailmelbin
```

---

### 3. Tag the Docker Image

```powershell
docker tag ecommerce-retail-api acrecommerceretailmelbin.azurecr.io/ecommerce-retail-api:latest
```

---

### 4. Push the Docker Image

```powershell
docker push acrecommerceretailmelbin.azurecr.io/ecommerce-retail-api:latest
```

---

### 5. Create Azure App Service

Create a Web App with these settings:

| Field | Value |
|---|---|
| Publish | Container |
| Operating System | Linux |
| Region | France Central |
| Image source | Azure Container Registry |
| Registry | `acrecommerceretailmelbin` |
| Image | `ecommerce-retail-api` |
| Tag | `latest` |
| Port | `8000` |

The deployed URL is:

```text
https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net
```

---

### 6. Configure Managed Identity

Enable system-assigned managed identity for the Web App:

```text
App Service → Identity → System assigned → On
```

Then assign the identity to Azure Container Registry:

```text
Container Registry → Access control (IAM) → Add role assignment
```

Use:

| Field | Value |
|---|---|
| Role | `AcrPull` |
| Assign access to | Managed identity |
| Managed identity type | App Service |
| Selected identity | `app-ecommerce-retail-api-melbin` |

---

### 7. Add App Service Environment Variables

Go to:

```text
App Service → Settings → Environment variables → App settings
```

Add the required non-secret runtime settings:

```text
APP_ENV=azure
AZURE_SQL_DRIVER=ODBC Driver 18 for SQL Server
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
WEBSITES_PORT=8000
```

Sensitive values should be configured later as Azure Key Vault references:

```text
AZURE_SQL_SERVER
AZURE_SQL_DATABASE
AZURE_SQL_USERNAME
AZURE_SQL_PASSWORD
JWT_SECRET_KEY
JWT_ADMIN_USERNAME
JWT_ADMIN_PASSWORD
JWT_ANALYST_USERNAME
JWT_ANALYST_PASSWORD
JWT_VIEWER_USERNAME
JWT_VIEWER_PASSWORD
```

Save and restart the Web App after settings are added.

For the final deployed project, SQL credentials, JWT signing secret, and demo JWT user credentials are stored in Azure Key Vault rather than directly in App Service configuration.

---

### 8. Verify Deployment

Run:

```powershell
python scripts\verify_azure_app_deployment.py
```

Expected result:

```text
Azure App deployment verification passed.
```

The report is saved to:

```text
data/processed/azure_app_deployment_verification_report.csv
```


## Azure Key Vault Setup

This section explains how Azure Key Vault is used to manage sensitive App Service runtime values.

### Prerequisites

Before configuring Key Vault, complete:

- Azure SQL Database setup
- Azure App Service deployment
- App Service managed identity setup
- Successful deployed API test

---

### 1. Create Azure Key Vault

Create a Key Vault with the following settings:

| Field | Value |
|---|---|
| Resource group | `rg-ecommerce-retail-intelligence` |
| Key vault name | `kvretailmelbin` |
| Region | `France Central` |
| Pricing tier | `Standard` |
| Permission model | Azure role-based access control |
| Soft-delete | Enabled |
| Purge protection | Disabled for portfolio flexibility |

---

### 2. Give Developer Secret Management Access

Because the vault uses Azure RBAC, the developer account needs permission to create and manage secrets.

Assign this role to the developer Azure user:

| Field | Value |
|---|---|
| Scope | Key Vault |
| Role | `Key Vault Secrets Officer` |
| Assign access to | User, group, or service principal |
| Member | Developer Azure account |

---

### 3. Add Secrets

Create these secrets in Key Vault:

| Secret name | Purpose |
|---|---|
| `azure-sql-server` | Azure SQL Server hostname |
| `azure-sql-database` | Azure SQL Database name |
| `azure-sql-username` | Azure SQL username |
| `azure-sql-password` | Azure SQL password |
| `jwt-secret-key` | JWT signing secret |
| `jwt-admin-username` | Demo admin username |
| `jwt-admin-password` | Demo admin password |
| `jwt-analyst-username` | Demo analyst username |
| `jwt-analyst-password` | Demo analyst password |
| `jwt-viewer-username` | Demo viewer username |
| `jwt-viewer-password` | Demo viewer password |

Recommended username values:

| Secret name | Value |
|---|---|
| `jwt-admin-username` | `admin` |
| `jwt-analyst-username` | `analyst` |
| `jwt-viewer-username` | `viewer` |

Generate strong JWT secret and password values locally with:

```powershell
python -c "import secrets; print('jwt-secret-key=' + secrets.token_urlsafe(64)); print('jwt-admin-password=' + secrets.token_urlsafe(24)); print('jwt-analyst-password=' + secrets.token_urlsafe(24)); print('jwt-viewer-password=' + secrets.token_urlsafe(24))"
```

For each secret:

| Field | Value |
|---|---|
| Upload options | Manual |
| Content type | Blank |
| Activation date | Blank |
| Expiration date | Blank |
| Enabled | Yes |

---

### 4. Give App Service Read Access

Assign this role to the App Service managed identity:

| Field | Value |
|---|---|
| Scope | Key Vault |
| Role | `Key Vault Secrets User` |
| Assign access to | Managed identity |
| Managed identity type | App Service |
| Selected identity | `app-ecommerce-retail-api-melbin` |

This allows App Service to read secret values from Key Vault.

---

### 5. Configure App Service Key Vault References

In App Service environment variables, replace sensitive values with Key Vault references.

Go to:

```text
App Services
→ app-ecommerce-retail-api-melbin
→ Settings
→ Environment variables
→ App settings
```

Use these references:

| App setting | Value |
|---|---|
| `AZURE_SQL_SERVER` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-server)` |
| `AZURE_SQL_DATABASE` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-database)` |
| `AZURE_SQL_USERNAME` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-username)` |
| `AZURE_SQL_PASSWORD` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-password)` |
| `JWT_SECRET_KEY` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-secret-key)` |
| `JWT_ADMIN_USERNAME` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-admin-username)` |
| `JWT_ADMIN_PASSWORD` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-admin-password)` |
| `JWT_ANALYST_USERNAME` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-analyst-username)` |
| `JWT_ANALYST_PASSWORD` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-analyst-password)` |
| `JWT_VIEWER_USERNAME` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-viewer-username)` |
| `JWT_VIEWER_PASSWORD` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-viewer-password)` |

Keep these non-secret settings as plain values:

| App setting | Value |
|---|---|
| `APP_ENV` | `azure` |
| `AZURE_SQL_DRIVER` | `ODBC Driver 18 for SQL Server` |
| `JWT_ALGORITHM` | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |
| `WEBSITES_PORT` | `8000` |

After saving, confirm that Key Vault references show as resolved in App Service configuration.

---

### 6. Restart and Test App Service

Restart the deployed API:

```text
App Service → Overview → Restart
```

Test the health endpoint:

```text
https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net/health/
```

Expected result:

```json
{
  "status": "ok",
  "service": "E-Commerce Retail Intelligence API",
  "database_connected": true
}
```

---

### 7. Run Key Vault Verification Script

Run:

```powershell
python scripts\verify_key_vault_setup.py
```

Expected result:

```text
Key Vault setup verification passed.
```

The report is saved to:

```text
data/processed/key_vault_setup_verification_report.csv
```

## Azure Monitoring Setup

This section explains how monitoring was configured for the deployed FastAPI API.

### Prerequisites

Before configuring monitoring, complete:

- Azure App Service deployment
- Azure Key Vault setup
- Successful deployed API test
- Successful `/health/` endpoint response

---

### 1. Enable App Service Logs

Go to:

```text
Azure Portal
→ App Services
→ app-ecommerce-retail-api-melbin
→ Monitoring
→ App Service logs
```

Configure:

| Setting | Value |
|---|---|
| Application logging | File System |
| Quota | 35 MB |
| Retention period | Short-term retention |

Save the configuration.

---

### 2. Verify Log Stream

Go to:

```text
App Services
→ app-ecommerce-retail-api-melbin
→ Monitoring
→ Log stream
```

Open the health endpoint in another browser tab:

```text
https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net/health/
```

Confirm that request or container activity appears in Log Stream.

---

### 3. Built-in Health Check Note

The project uses Application Insights availability testing for the `/health/` endpoint.

Built-in App Service Health Check can also be enabled on Basic B1 or higher App Service plans, but Application Insights availability testing remains the documented monitoring approach for this portfolio project.

---

### 4. Create Application Insights

Create an Application Insights resource:

| Field | Value |
|---|---|
| Resource group | `rg-ecommerce-retail-intelligence` |
| Name | `appi-ecommerce-retail-api` |
| Region | France Central |
| Resource mode | Workspace-based |

Use or create a Log Analytics workspace in the same subscription.

---

### 5. Connect App Service to Application Insights

Go to:

```text
App Services
→ app-ecommerce-retail-api-melbin
→ Settings
→ Application Insights
```

Choose:

| Field | Value |
|---|---|
| Application Insights | Enable |
| Link option | Select existing resource |
| Resource | `appi-ecommerce-retail-api` |
| Stack | Python |

Apply the setting and restart the Web App.

---

### 6. Create Availability Test

Go to:

```text
Application Insights
→ appi-ecommerce-retail-api
→ Investigate
→ Availability
→ Create Standard test
```

Configure:

| Field | Value |
|---|---|
| Test name | `fastapi-health-check` |
| URL | `https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net/health/` |
| HTTP method | GET |
| Expected status code | 200 |
| Frequency | 5 minutes |
| Timeout | 120 seconds |
| Test locations | 5 selected |
| SSL certificate validity | Enabled |
| Retries | Enabled |
| Alerts | Enabled |

Wait for the first test result.

Expected result:

```text
Availability result: Successful
```

---

### 7. Alert Rule

An automatic alert rule is created for the availability test.

The final rule monitors:

| Field | Value |
|---|---|
| Signal | Availability |
| Condition | Failed locations >= 2 |
| Severity | 1 - Error |
| Scope | `appi-ecommerce-retail-api` |

A custom action group was not required for the final setup.

---

### 8. Run Monitoring Verification Script

Run:

```powershell
python scripts\verify_azure_monitoring_setup.py
```

Expected result:

```text
Azure monitoring setup verification passed.
```

Output report:

```text
data/processed/azure_monitoring_setup_verification_report.csv
```

## Final Technical Verification Checklist

Before moving to portfolio packaging, confirm that the technical platform is complete.

### Local development checks

```powershell
python scripts\run_tests.py
```

Expected result:

```text
Automated tests passed
```

### Docker check

```powershell
python scripts\verify_docker_setup.py
```

Expected result:

```text
Docker setup verification passed
```

### Azure Blob Storage check

```powershell
python scripts\verify_azure_blob_setup.py
```

Expected result:

```text
Azure Blob Storage setup verification passed
```

### Azure SQL check

```powershell
python scripts\verify_azure_sql_setup.py
```

Expected result:

```text
Azure SQL setup verification passed
```

### Azure Data Factory checks

```powershell
python scripts\verify_adf_setup.py
python scripts\verify_adf_pipeline_output.py
```

Expected result:

```text
ADF setup verification passed
ADF pipeline output verification passed
```

### Azure App Service deployment check

```powershell
python scripts\verify_azure_app_deployment.py
```

Expected result:

```text
Azure App deployment verification passed
```

### Azure Key Vault check

```powershell
python scripts\verify_key_vault_setup.py
```

Expected result:

```text
Key Vault setup verification passed
```

### Azure Monitoring check

```powershell
python scripts\verify_azure_monitoring_setup.py
```

Expected result:

```text
Azure monitoring setup verification passed
```

---

## GitHub Actions CI/CD Setup

The project includes GitHub Actions workflows for Continuous Integration and Continuous Deployment.

| Workflow | File | Purpose |
|---|---|---|
| CI Pipeline | `.github/workflows/ci.yml` | Validates code, imports, setup, and Docker build |
| CD Pipeline | `.github/workflows/cd-azure-app.yml` | Builds the Docker image, pushes it to ACR, deploys to Azure App Service, and verifies `/health/` |

---

### GitHub Secrets Required for CD

The CD workflow uses GitHub repository secrets.

| Secret | Purpose |
|---|---|
| `AZURE_CREDENTIALS` | Azure service principal JSON |
| `ACR_LOGIN_SERVER` | Azure Container Registry login server |
| `AZURE_WEBAPP_NAME` | Azure App Service name |
| `AZURE_RESOURCE_GROUP` | Azure resource group |
| `AZURE_APP_BASE_URL` | Deployed API base URL |

---

### CD Deployment Flow

```text
Push to main
        ↓
GitHub Actions CD workflow
        ↓
Azure login using service principal
        ↓
Docker image build
        ↓
Push image to Azure Container Registry
        ↓
Ensure App Service managed identity exists
        ↓
Ensure App Service has AcrPull permission
        ↓
Configure managed identity ACR image pull
        ↓
Set App Service container image
        ↓
Restart Azure App Service
        ↓
Verify /health/ endpoint
```

---

### Important Runtime Requirement

The CD workflow verifies the deployed API using:

```text
/health/
```

Because the health endpoint checks Azure SQL connectivity, Azure SQL Database must be online when the CD workflow runs.

Expected health response:

```json
{
  "status": "ok",
  "service": "E-Commerce Retail Intelligence API",
  "database_connected": true
}
```

---

### CI/CD Verification

After pushing to GitHub, confirm both workflows pass:

```text
CI Pipeline: Passed
CD - Deploy FastAPI Container to Azure App Service: Passed
```

Screenshots:

```text
docs/images/02a_ci_pipeline_success.png
docs/images/02b_cd_pipeline_success.png
```

Full CI/CD documentation:

```text
docs/azure_ci_cd.md
```

## Final Technical Completion Criteria

The project is technically complete when the following are done:

```text
Raw data ingestion completed
Data quality validation completed
Staging and warehouse models completed
dbt tests and documentation completed
Operational anomaly detection completed
API backend completed
Authentication and RBAC completed
Automated tests completed
Docker setup completed
GitHub Actions CI/CD completed
Azure Blob Storage completed
Azure SQL Database completed
Azure Data Factory completed
Azure App Service deployment completed
Azure Key Vault integration completed
Azure Monitoring completed
Final architecture documentation completed
```

After this checklist is complete, the project can move to portfolio packaging and recruiter-facing presentation.