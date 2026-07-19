# Setup Guide

## Purpose

This setup guide explains how to run and validate the **E-Commerce Retail Intelligence Platform** locally.

The guide covers:

- Python environment setup
- Dependency installation
- Automated tests
- Docker execution
- GitHub Actions CI-equivalent checks

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

The project uses demo API keys for local testing.

Create a local `.env` file from `.env.example` if needed:

```powershell
copy .env.example .env
```

The demo API keys are:

| Role | Demo Key |
|---|---|
| Admin | `admin-demo-key` |
| Analyst | `analyst-demo-key` |
| Viewer | `viewer-demo-key` |

The `.env` file should not be committed to GitHub.

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
uvicorn src.api.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Useful local API endpoints:

```text
/
```

```text
/health/
```

```text
/health/status
```

Protected endpoints require the `X-API-Key` header.

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

Add:

```text
APP_ENV=azure
AZURE_SQL_SERVER=<your-server-name>.database.windows.net
AZURE_SQL_DATABASE=sqldb-ecommerce-retail-intelligence
AZURE_SQL_USERNAME=<your-sql-username>
AZURE_SQL_PASSWORD=<your-sql-password>
AZURE_SQL_DRIVER=ODBC Driver 18 for SQL Server
ADMIN_API_KEY=admin-demo-key
ANALYST_API_KEY=analyst-demo-key
VIEWER_API_KEY=viewer-demo-key
WEBSITES_PORT=8000
```

Save and restart the Web App.

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
| `admin-api-key` | Admin API key |
| `analyst-api-key` | Analyst API key |
| `viewer-api-key` | Viewer API key |

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
| `ADMIN_API_KEY` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=admin-api-key)` |
| `ANALYST_API_KEY` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=analyst-api-key)` |
| `VIEWER_API_KEY` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=viewer-api-key)` |

Keep these non-secret settings as plain values:

| App setting | Value |
|---|---|
| `APP_ENV` | `azure` |
| `AZURE_SQL_DRIVER` | `ODBC Driver 18 for SQL Server` |
| `WEBSITES_PORT` | `8000` |

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