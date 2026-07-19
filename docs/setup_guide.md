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