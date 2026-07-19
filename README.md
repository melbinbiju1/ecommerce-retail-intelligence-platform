# E-Commerce Retail Intelligence Platform

![CI Pipeline](https://github.com/melbinbiju1/ecommerce-retail-intelligence-platform/actions/workflows/ci.yml/badge.svg)

An end-to-end Data Engineering and AI Business Insights platform built using the Olist Brazilian E-Commerce dataset.

## Project Objective

This project builds a modern e-commerce retail intelligence platform that ingests raw order, customer, product, seller, payment, review, delivery, and geolocation data, transforms it into a warehouse model, produces business KPIs, detects operational anomalies, and provides AI-powered business insights.

## Core Dataset

Main dataset: **Olist Brazilian E-Commerce Public Dataset**

The Olist dataset contains real anonymised e-commerce order data, including:

* Orders
* Customers
* Products
* Sellers
* Payments
* Reviews
* Delivery timestamps
* Geolocation data
* Product category translation

## Key Features

* Batch ETL pipeline
* Raw, staging, warehouse, and KPI data layers
* Data quality validation
* Star schema data warehouse
* Operational metrics layer
* Operational anomaly detection
* Event-driven operational alert pipeline
* Delivery delay anomaly detection
* Seller performance anomaly detection
* Payment anomaly detection
* Freight cost anomaly detection
* Review score anomaly detection
* Cancellation anomaly detection
* Power BI executive dashboard
* FastAPI backend
* JWT authentication
* Role-based access control
* AI business insights assistant
* Docker containerisation
* GitHub Actions CI/CD
* Azure Blob Storage
* Azure SQL Database
* Azure Data Factory
* Azure Key Vault
* Azure Monitor
* Logging, error handling, monitoring, and health checks
* Unit tests, integration tests, and API tests
* Complete documentation, architecture diagram, database diagram, and setup guide

## Business Problem

E-commerce businesses need reliable visibility into sales performance, customer behaviour, seller performance, delivery delays, payment patterns, product demand, customer satisfaction, and operational risks.

This platform helps decision-makers monitor performance, detect unusual business patterns, and receive AI-assisted explanations and recommendations.

## Target Users

* E-commerce Operations Manager
* Sales Manager
* Logistics Manager
* Seller Performance Manager
* Finance Manager
* Executive Leadership
* Data and BI Team

## Technology Stack

| Area            | Tools                  |
| --------------- | ---------------------- |
| Programming     | Python                 |
| Data Processing | Pandas, SQL            |
| Local Database  | SQLite                 |
| Cloud Database  | Azure SQL Database     |
| Cloud Storage   | Azure Blob Storage     |
| Orchestration   | Azure Data Factory     |
| API             | FastAPI                |
| Authentication  | JWT                    |
| BI              | Power BI               |
| AI              | OpenAI / Azure OpenAI  |
| DevOps          | Docker, GitHub Actions |
| Monitoring      | Logging, Azure Monitor |
| Secrets         | Azure Key Vault        |
| Testing         | pytest                 |

## Data Architecture

```text
Olist CSV Files
      ↓
Raw Data Layer
      ↓
Raw Data Quality Checks
      ↓
Staging Layer
      ↓
Warehouse Star Schema
      ↓
KPI Views
      ↓
Operational Metrics and Anomaly Detection
      ↓
Power BI Dashboard / FastAPI / AI Assistant
```

## Project Layers

### Raw Layer

Stores the original Olist source data with minimal changes.

### Staging Layer

Cleans and standardises raw data, including date conversion, text standardisation, product category translation, and delivery flags.

### Warehouse Layer

Creates business-ready dimension and fact tables using a star schema.

### KPI Layer

Creates trusted SQL views for Power BI, FastAPI, and the AI assistant.

### Operational Anomaly Layer

Detects unusual operational patterns such as revenue drops, delivery delay spikes, seller performance issues, payment anomalies, freight cost anomalies, low review patterns, and cancellation spikes.

### AI Business Insights Layer

Uses trusted KPI and anomaly outputs to generate business explanations and recommendations.

## Current Local Development Flow

```text
CSV Files
   ↓
Python Ingestion Scripts
   ↓
SQLite Raw Tables
   ↓
Data Quality Checks
   ↓
Staging SQL Transformations
   ↓
Warehouse Tables
   ↓
KPI Views
   ↓
Operational Anomaly Detection
```

## Planned Cloud Architecture

```text
Azure Blob Storage
      ↓
Azure Data Factory
      ↓
Azure SQL Database
      ↓
Warehouse Tables + KPI Views
      ↓
Power BI + FastAPI
      ↓
AI Business Insights Assistant
      ↓
Azure Key Vault + Azure Monitor
```

## Portfolio Value

This project demonstrates practical skills in:

* Data Engineering
* Analytics Engineering
* SQL Data Warehousing
* Data Quality Validation
* Operational Analytics
* Anomaly Detection
* Business Intelligence
* API Development
* AI Business Insights
* Cloud Deployment
* CI/CD
* Testing and Monitoring

## Governance, Lineage, and Cloud Migration

The project includes documentation for governance, lineage, and Azure SQL migration readiness.

| Document | Purpose |
|---|---|
| `docs/data_governance.md` | Explains data ownership assumptions, quality controls, auditability, sensitive data handling, and AI governance |
| `docs/data_lineage.md` | Explains how data flows from Olist CSV files to raw tables, dbt models, KPI views, Power BI, FastAPI, and AI outputs |
| `docs/azure_sql_migration_plan.md` | Explains how the local SQLite project will be migrated to Azure SQL Database and Azure Data Factory |

## FastAPI Backend

The project includes a FastAPI backend that exposes curated business and operational data through REST API endpoints.

The API reads from the SQLite database and serves dbt-built KPI views, warehouse outputs, operational anomaly alerts, and risk summaries.

### Run the API

```powershell
uvicorn src.api.main:app --reload
```

## API Authentication and RBAC

The FastAPI backend includes API-key based authentication and role-based access control.

Protected endpoints require the `X-API-Key` request header.

### Demo API Keys

| Role | Demo Key | Access Level |
|---|---|---|
| Admin | `admin-demo-key` | Full API access |
| Analyst | `analyst-demo-key` | Executive and operational read access |
| Viewer | `viewer-demo-key` | Limited executive read access |

### Role Access Matrix

| Endpoint | Admin | Analyst | Viewer |
|---|---:|---:|---:|
| `/` | Yes | Yes | Yes |
| `/health/` | Yes | Yes | Yes |
| `/executive/summary` | Yes | Yes | Yes |
| `/executive/monthly-sales` | Yes | Yes | Yes |
| `/executive/top-products` | Yes | Yes | No |
| `/executive/top-sellers` | Yes | Yes | No |
| `/executive/customer-states` | Yes | Yes | No |
| `/operations/alert-summary` | Yes | Yes | No |
| `/operations/alerts-by-type` | Yes | Yes | No |
| `/operations/alerts-by-severity` | Yes | Yes | No |
| `/operations/recent-alerts` | Yes | Yes | No |
| `/operations/high-risk-sellers` | Yes | Yes | No |
| `/operations/high-risk-categories` | Yes | Yes | No |
| `/operations/risk-summary` | Yes | Yes | No |
| `/insights/executive-summary` | Yes | Yes | Yes |
| `/insights/sales-performance` | Yes | Yes | No |
| `/insights/operational-risk` | Yes | Yes | No |
| `/insights/recommendations` | Yes | Yes | No |
| `/insights/llm-context` | Yes | No | No |

### Example Request

```powershell
curl -H "X-API-Key: analyst-demo-key" http://127.0.0.1:8000/operations/alert-summary
```

## AI-Ready Business Insights Assistant

The project includes an AI-ready business insights layer that generates executive summaries, sales insights, operational risk explanations, and recommended business actions from trusted data platform outputs.

The first version is deterministic and rule-based. This makes the insights explainable, reproducible, and free from external API costs. The layer is also designed to be LLM-ready by generating a structured context file that can be passed to a future Large Language Model.

### Why This Design Was Used

The insights assistant does not read directly from raw source CSV files. It uses curated warehouse tables, dbt models, KPI views, and operational risk views.

This design reduces the risk of unsupported or unreliable AI responses because the insights are grounded in validated business data.

### Trusted Data Sources Used by the Insights Layer

| Source | Purpose |
|---|---|
| `fact_sales` | Calculates total revenue, total orders, freight value, and average order value |
| `dim_customer` | Calculates unique customer count |
| `dim_seller` | Calculates seller count |
| `vw_monthly_sales` | Provides recent meaningful monthly revenue and order trends |
| `vw_product_performance` | Identifies high-performing product categories |
| `vw_customer_state_performance` | Identifies strong customer geography areas |
| `vw_operational_alert_summary` | Summarises total, high, and medium severity operational alerts |
| `vw_operational_alerts_by_type` | Identifies the most common operational anomaly types |
| `vw_high_risk_sellers` | Highlights sellers with delivery or review risk |
| `vw_high_risk_categories` | Highlights product categories with operational risk |

### Insight Outputs

| Output | Purpose |
|---|---|
| Executive Summary | Summarises revenue, orders, customers, sellers, average order value, and recent meaningful sales trends |
| Sales Performance | Highlights product category and customer geography performance |
| Operational Risk Summary | Explains anomaly alerts, severity, high-risk sellers, and high-risk categories |
| Recommendations | Provides practical business actions based on KPI and operational risk outputs |
| LLM Context Summary | Creates structured, governed context for future LLM integration |

### API Endpoints

| Endpoint | Access |
|---|---|
| `/insights/executive-summary` | Admin, Analyst, Viewer |
| `/insights/sales-performance` | Admin, Analyst |
| `/insights/operational-risk` | Admin, Analyst |
| `/insights/recommendations` | Admin, Analyst |
| `/insights/llm-context` | Admin only |

### Generate Local Insight Files

```powershell
python scripts\generate_ai_business_insights.py
python scripts\generate_llm_context.py
```

## API Logging, Error Handling, and Health Checks

The FastAPI backend includes logging, centralised error handling, and health check endpoints.

### Logging

API request and error logs are written to:

`logs/api.log`

The logger uses rotating file handling to prevent the log file from growing indefinitely.

### Health Endpoints

| Endpoint | Purpose |
|---|---|
| `/health/` | Checks whether the API can connect to the database |
| `/health/status` | Checks database connectivity and important warehouse/KPI/operational objects |

### Error Handling

The API includes middleware that logs:

- Request method
- Request path
- Response status code
- Request duration
- Unexpected errors

Unexpected server errors return a safe JSON response instead of exposing internal stack traces to API users.

This makes the backend easier to debug and closer to production API practices.

 ## Automated Testing

The project includes an automated test suite covering the database layer, FastAPI endpoints, authentication and RBAC rules, AI-ready insights, and important pipeline outputs.

The tests are organised into unit, API, and integration test folders to reflect a professional testing structure.

 ### Test Result

Latest local test run:

```text
32 passed, 1 warning
```

## Docker Containerisation

The FastAPI backend is containerised using Docker so the API can run in a clean, reproducible environment outside the local Python virtual environment.

Docker is used in this project to demonstrate:

- API containerisation
- Reproducible local execution
- Dependency packaging
- Deployment readiness
- Preparation for CI/CD and Azure deployment

### Docker Summary

| Item | Description |
|---|---|
| Docker image | Packages the FastAPI backend and Python dependencies |
| Docker container | Runs the FastAPI API on port `8000` |
| Local database | `retail_intelligence.db` is mounted into the container at runtime |
| API framework | FastAPI with Uvicorn |
| Authentication | API-key authentication and role-based access control remain active |
| Future cloud database | Azure SQL Database |
| Detailed documentation | Full Docker instructions are available in `docker/README.md` |

### Build Docker Image

From the project root:

```powershell
docker build -t ecommerce-retail-api .
```

### Run Docker Container

```powershell
docker run --name ecommerce-retail-api-container -p 8000:8000 -v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db ecommerce-retail-api
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

### Run Container in Detached Mode

Detached mode runs the API container in the background:

```powershell
docker run -d --name ecommerce-retail-api-container -p 8000:8000 -v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db ecommerce-retail-api
```

View running containers:

```powershell
docker ps
```

View logs:

```powershell
docker logs ecommerce-retail-api-container
```

Stop and remove the container:

```powershell
docker stop ecommerce-retail-api-container
docker rm ecommerce-retail-api-container
```

### Docker Documentation

Detailed Docker setup, troubleshooting, command reference, and local-vs-cloud notes are available in:

```text
docker/README.md
```

### Local vs Cloud Note

The local Docker version mounts the SQLite database file into the container at runtime so the API can serve local portfolio data without making the Docker image unnecessarily large.

In the Azure version, the API will connect to Azure SQL Database instead of using the local SQLite database file. Secrets will be managed through Azure Key Vault.


## GitHub Actions CI Pipeline

The project includes a GitHub Actions CI pipeline to automatically validate the repository when code is pushed to GitHub.

The workflow file is located at:

```text
.github/workflows/ci.yml
```

### CI Pipeline Purpose

The CI pipeline checks that the project can be installed, imported, verified, and containerised successfully in a clean GitHub Actions environment.

This provides a Continuous Integration foundation before the later Azure deployment phases.

### CI Pipeline Checks

| Step | Purpose |
|---|---|
| Checkout repository | Loads the project files into the GitHub Actions runner |
| Confirm database is not tracked | Ensures the large local SQLite database is not committed to GitHub |
| Set up Python | Installs Python 3.10 |
| Install dependencies | Installs packages from `requirements.txt` |
| Validate Python syntax | Runs `python -m compileall src scripts` |
| Validate imports | Confirms core API and AI insight modules can be imported |
| Verify Docker setup | Runs `scripts/verify_docker_setup.py` |
| Verify CI setup | Runs `scripts/verify_ci_setup.py` |
| Build Docker image | Confirms the Docker image can be built successfully |

### Trigger Events

The CI pipeline runs on:

- Pushes to the `main` or `master` branch
- Pull requests targeting `main` or `master`
- Manual workflow dispatch from GitHub Actions

### Local Equivalent Commands

Before pushing to GitHub, the main CI checks can be run locally:

```powershell
pip install -r requirements.txt
python -m compileall src scripts
python scripts\verify_docker_setup.py
python scripts\verify_ci_setup.py
docker build -t ecommerce-retail-api .
```

### CI Database Design

The project does not commit the local SQLite database to GitHub because `retail_intelligence.db` is a large generated file.

The local Docker version mounts the SQLite database at runtime for local demonstration.

In GitHub Actions, the CI pipeline uses database-independent validation checks.

Full database/API tests are run locally for now and can be expanded in CI later after Azure SQL Database or a smaller CI test database is introduced.

### CI/CD Scope Note

This phase implements Continuous Integration.

It does not automatically deploy the application to Azure yet.

Continuous Deployment will be added later after the Azure SQL Database, Azure Key Vault, Azure App hosting, and Azure Monitor phases are completed.


## Azure Blob Storage

The project uses Azure Blob Storage as the cloud landing zone for raw e-commerce data.

Raw Olist CSV files are uploaded to a private Azure Blob container using a Python upload script.

### Azure Blob Structure

```text
ecommerce-retail-data/
    raw/
        olist/
            olist_customers_dataset.csv
            olist_orders_dataset.csv
            olist_order_items_dataset.csv
            ...
```

### Azure Blob Scripts

| Script | Purpose |
|---|---|
| `scripts/upload_raw_data_to_blob.py` | Uploads local raw CSV files to Azure Blob Storage |
| `scripts/verify_azure_blob_setup.py` | Verifies local files, documentation, dependencies, and uploaded blobs |

### Azure Blob Reports

| Report | Purpose |
|---|---|
| `data/processed/azure_blob_upload_report.csv` | Stores raw file upload results |
| `data/processed/azure_blob_setup_verification_report.csv` | Stores Azure Blob verification results |

Detailed documentation is available in:

```text
docs/azure_blob_storage.md
```

The local `.env` file stores the Azure Storage connection string for this phase. In a later phase, secrets will be moved to Azure Key Vault.


## Azure SQL Database

The project uses Azure SQL Database as the cloud serving database for curated analytical data.

Azure SQL is used to store selected warehouse, fact, dimension, operational, anomaly, and event pipeline outputs that were generated by the local transformation pipeline.

### Azure SQL Purpose

Azure SQL Database supports the cloud serving layer of the project.

```text
Azure Blob Storage
        ↓
Raw Olist CSV files
        ↓
Local Python + dbt transformation pipeline
        ↓
Curated warehouse and operational outputs
        ↓
Azure SQL Database
        ↓
Future FastAPI / Power BI cloud serving
```

### Objects Loaded to Azure SQL

The Azure SQL migration includes:

| Object Group | Examples |
|---|---|
| Dimension tables | `dim_date`, `dim_customer`, `dim_product`, `dim_seller` |
| Fact tables | `fact_sales`, `fact_delivery`, `fact_payments`, `fact_reviews` |
| Operational tables | `ops_daily_metrics`, `ops_seller_metrics`, `ops_category_metrics` |
| Anomaly tables | `ops_anomaly_rules`, `ops_anomaly_alerts` |
| Event pipeline tables | `ops_event_log`, `ops_event_records` |

### Azure SQL Scripts

| Script | Purpose |
|---|---|
| `scripts/test_azure_sql_connection.py` | Tests Azure SQL connectivity |
| `scripts/migrate_curated_data_to_azure_sql.py` | Migrates curated SQLite tables into Azure SQL |
| `scripts/verify_azure_sql_setup.py` | Verifies Azure SQL setup and loaded table row counts |

### Azure SQL Reports

| Report | Purpose |
|---|---|
| `data/processed/azure_sql_connection_test_report.csv` | Stores Azure SQL connection test result |
| `data/processed/azure_sql_migration_report.csv` | Stores migration status and row counts |
| `data/processed/azure_sql_setup_verification_report.csv` | Stores Azure SQL verification results |

### Azure SQL Verification Result

The Azure SQL verification confirmed that the expected curated objects were loaded successfully.

Example loaded row counts:

| Table | Rows |
|---|---:|
| `dim_customer` | 99,441 |
| `dim_product` | 32,951 |
| `fact_sales` | 112,650 |
| `fact_delivery` | 99,441 |
| `fact_payments` | 103,886 |
| `fact_reviews` | 99,224 |
| `ops_anomaly_alerts` | 696 |
| `ops_event_records` | 100 |

Detailed documentation is available in:

```text
docs/azure_sql_database.md
```

Real Azure SQL credentials are stored only in the local `.env` file and are not committed to GitHub. In a later phase, secrets will be managed through Azure Key Vault.


## Azure Data Factory

The project uses Azure Data Factory as the cloud orchestration layer.

In this phase, ADF is used to copy a raw Olist CSV file from Azure Blob Storage into an Azure SQL staging table.

### ADF Pipeline

```text
Azure Blob Storage
        ↓
Azure Data Factory Copy Activity
        ↓
Azure SQL Database staging table
```

### ADF Objects

| Object | Name |
|---|---|
| Data Factory | `adf-ecommerce-retail-intelligence` |
| Pipeline | `pl_copy_olist_orders_blob_to_sql` |
| Source linked service | `ls_azure_blob_olist_raw` |
| Sink linked service | `ls_azure_sql_retail` |
| Source dataset | `ds_blob_olist_orders_raw_csv` |
| Sink dataset | `ds_sql_adf_stg_orders_raw` |
| Sink table | `dbo.adf_stg_orders_raw` |

### ADF Verification

The pipeline output is verified using:

```powershell
python scripts\verify_adf_pipeline_output.py
```

Verification report:

```text
data/processed/adf_pipeline_output_verification_report.csv
```

Detailed documentation is available in:

```text
docs/azure_data_factory.md
```