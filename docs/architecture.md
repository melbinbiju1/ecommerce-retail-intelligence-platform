# Architecture Documentation

## Project Name

**E-Commerce Retail Intelligence Platform**

## Purpose

This document explains the architecture of the E-Commerce Retail Intelligence Platform.

The project is designed as an end-to-end Data Engineering and AI Business Insights platform using the Olist Brazilian E-Commerce dataset.

The platform follows a layered architecture:

1. Raw data ingestion
2. Raw data validation
3. Staging transformation
4. Warehouse modelling
5. KPI views
6. Operational metrics
7. Operational anomaly detection
8. Event-driven operational alert processing
9. Power BI reporting
10. FastAPI backend
11. AI business insights assistant
12. Azure deployment

## Architecture Documentation Index

The project contains multiple architecture documents, each with a different purpose.

| Document | Purpose |
|---|---|
| `docs/final_architecture.md` | Clean final end-to-end architecture summary of the implemented platform |
| `docs/technical_architecture.md` | Detailed technical design decisions, runtime modes, trade-offs, security, deployment, and monitoring architecture |
| `docs/system_flow.md` | Step-by-step explanation of data flow, API request flow, deployment flow, secret flow, and monitoring flow |

Use this file, `docs/architecture.md`, as the detailed working architecture document created throughout the project.

For a polished final overview, start with:

```text
docs/final_architecture.md
```

## 1. High-Level Architecture

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

---

## 2. Local Development Architecture

During local development, the project uses CSV files, Python scripts, SQLite, SQL files, and local folders.

```text
data/raw/
   ↓
Python Ingestion Scripts
   ↓
SQLite Raw Tables
   ↓
Raw Data Quality Checks
   ↓
Staging SQL Transformations
   ↓
Warehouse Tables
   ↓
KPI SQL Views
   ↓
Operational Metrics
   ↓
Operational Anomaly Alerts
   ↓
Power BI / FastAPI / AI Assistant
```

### Local Components

| Component                | Purpose                                                                |
| ------------------------ | ---------------------------------------------------------------------- |
| `data/raw/`              | Stores original Olist CSV files                                        |
| `scripts/`               | Contains pipeline execution scripts                                    |
| `src/`                   | Contains reusable project code                                         |
| `retail_intelligence.db` | Local SQLite database                                                  |
| `logs/`                  | Stores pipeline logs                                                   |
| `data/processed/`        | Stores validation and verification reports                             |
| `sql/`                   | Stores SQL scripts for staging, warehouse, KPI, and operational layers |
| `docs/`                  | Stores project documentation                                           |

---

## 3. Data Layer Architecture

The data platform is divided into four main data layers.

```text
Raw Layer
   ↓
Staging Layer
   ↓
Warehouse Layer
   ↓
KPI Layer
```

---

## 3.1 Raw Layer

The raw layer stores the original source data with minimal changes.

Example raw tables:

```text
raw_customers
raw_orders
raw_order_items
raw_order_payments
raw_order_reviews
raw_products
raw_sellers
raw_geolocation
raw_product_category_translation
```

Purpose of the raw layer:

* Preserve original source data
* Support auditability
* Allow reprocessing if business logic changes
* Store metadata such as source file and load timestamp

---

## 3.2 Staging Layer

The staging layer stores cleaned and standardised data.

Example staging tables:

```text
stg_customers
stg_orders
stg_order_items
stg_order_payments
stg_order_reviews
stg_products
stg_sellers
stg_geolocation
stg_product_category_translation
```

Main staging transformations:

* Standardise text formatting
* Convert date fields into datetime format
* Translate product categories into English
* Create delivery flags
* Create delivery duration fields
* Deduplicate geolocation data
* Prepare data for warehouse modelling

---

## 3.3 Warehouse Layer

The warehouse layer stores business-ready fact and dimension tables.

```text
dim_date
dim_customer
dim_product
dim_seller

fact_sales
fact_delivery
fact_payments
fact_reviews
```

The warehouse uses a star schema structure.

```text
dim_date       dim_customer       dim_product       dim_seller
    │               │                  │                │
    └───────────────┴──────────────────┴────────────────┘
                              │
                         fact_sales
```

Purpose of the warehouse layer:

* Support reporting
* Improve query performance
* Create business-friendly models
* Separate analytics logic from raw source data
* Support Power BI, APIs, and AI insight generation

---

## 3.4 KPI Layer

The KPI layer contains business-ready SQL views used by Power BI, FastAPI, and the AI assistant.

Example KPI views:

```text
vw_executive_summary
vw_monthly_sales
vw_product_performance
vw_seller_performance
vw_customer_state_performance
vw_delivery_performance
vw_payment_analysis
vw_review_analysis
vw_late_delivery_by_state
vw_category_review_performance
```

Purpose of the KPI layer:

* Provide trusted business metrics
* Avoid repeated calculations in Power BI
* Make API endpoints easier to build
* Provide clean context for AI-generated business insights

---

## 4. Operational Metrics Architecture

The operational metrics layer creates daily and business-area-level metrics from real Olist data.

```text
Warehouse Tables + KPI Views
      ↓
Operational Daily Metrics
      ↓
Operational Anomaly Rules
      ↓
Operational Anomaly Alerts
```

Example operational metrics:

* Daily revenue
* Daily order count
* Average order value
* Late delivery count
* Late delivery rate
* Cancelled order count
* Average review score
* Low review count
* Average freight value
* Seller-level delivery performance
* Product category performance

Purpose of the operational metrics layer:

* Prepare clean metrics for anomaly detection
* Support operational risk analysis
* Feed Power BI operational alert pages
* Provide trusted context for the AI assistant

---

## 5. Operational Anomaly Detection Architecture

The anomaly detection layer identifies unusual business behaviour from the real Olist dataset.

```text
Operational Metrics
      ↓
Rule-Based Anomaly Detection
      ↓
Operational Anomaly Alerts
      ↓
Power BI / FastAPI / AI Assistant
```

Planned anomaly types:

```text
REVENUE_DROP
ORDER_VOLUME_SPIKE
DELIVERY_DELAY_SPIKE
SELLER_PERFORMANCE_RISK
PAYMENT_VALUE_ANOMALY
FREIGHT_COST_SPIKE
LOW_REVIEW_SPIKE
CANCELLATION_SPIKE
CATEGORY_REVENUE_DROP
```

Example anomaly alert fields:

```text
alert_id
alert_date
alert_type
severity
business_area
metric_name
actual_value
expected_value
difference_value
difference_percentage
alert_description
recommended_action
created_at
```

Purpose:

* Detect operational risks
* Highlight unusual business patterns
* Support executive decision-making
* Provide AI assistant context

---

## 6. Event-Driven Operational Alert Pipeline

The project includes a local event-driven operational alert pipeline. This simulates how a real company might process new operational event files.

```text
New Operational Event CSV
      ↓
data/operational_events/incoming/
      ↓
process_operational_event_files.py
      ↓
Schema Validation
      ↓
Record Validation
      ↓
Valid Records → ops_event_records
Invalid Records → ops_event_failed_records
      ↓
File moved to processed/failed folder
      ↓
ops_event_log updated
```

### Event Pipeline Folders

```text
data/operational_events/incoming/
data/operational_events/processed/
data/operational_events/failed/
```

### Event Pipeline Tables

```text
ops_event_log
ops_event_records
ops_event_failed_records
```

### Supported Operational Event Types

```text
LATE_DELIVERY
PAYMENT_FAILURE
LOW_REVIEW
ORDER_CANCELLED
HIGH_FREIGHT_COST
SELLER_DELAY_RISK
REVENUE_DROP
CATEGORY_DEMAND_DROP
```

### Purpose

This pipeline demonstrates an event-driven pattern.

In the local version, the trigger is simulated by placing a file into an incoming folder.

In the Azure version, this will be replaced by Azure Blob Storage and Azure Data Factory triggers.

---

## 7. Power BI Architecture

Power BI connects to the KPI views, warehouse tables, and operational anomaly tables.

```text
Warehouse Tables + KPI Views + Operational Alerts
      ↓
Power BI Data Model
      ↓
Executive Dashboard
```

### Planned Dashboard Pages

| Page                       | Purpose                                                                      |
| -------------------------- | ---------------------------------------------------------------------------- |
| Executive Overview         | Revenue, orders, sales trends, and key KPIs                                  |
| Sales Performance          | Monthly sales, revenue trends, average order value                           |
| Product Performance        | Category revenue, item sales, and top product categories                     |
| Seller Performance         | Seller revenue, seller location, and delivery patterns                       |
| Delivery Performance       | Delivery delays, delivery duration, and late orders                          |
| Customer Geography         | Revenue and orders by customer state                                         |
| Payment Analysis           | Payment methods, installments, and payment value                             |
| Review Analysis            | Review scores and customer satisfaction patterns                             |
| Operational Anomaly Alerts | Revenue, delivery, seller, payment, freight, review, and cancellation alerts |
| AI Insights                | AI-generated business explanations and recommendations                       |

---

## 8. FastAPI Architecture

The FastAPI backend will expose business data through secure REST API endpoints.

```text
FastAPI
   ↓
Authentication Layer
   ↓
Role-Based Access Control
   ↓
KPI / Operational Risk / AI Endpoints
   ↓
SQLite locally or Azure SQL in cloud
```

### Planned API Endpoints

```text
GET /health
POST /auth/login
GET /kpis/executive-summary
GET /kpis/monthly-sales
GET /kpis/product-performance
GET /kpis/seller-performance
GET /delivery/performance
GET /operations/daily-metrics
GET /operations/anomalies
GET /operations/events
GET /operations/risk-summary
POST /ai/ask
```

Purpose:

* Expose trusted business KPIs
* Expose operational anomaly alerts
* Support AI business insight generation
* Demonstrate backend engineering practices

---

## 9. AI Business Insights Architecture

The AI assistant will not use raw data directly. It will use trusted KPI views, operational metrics, and anomaly alert outputs.

```text
User Question
      ↓
FastAPI AI Endpoint
      ↓
Fetch trusted KPI/anomaly/operational context
      ↓
Send structured context to LLM
      ↓
Return business explanation and recommendations
```

Example AI questions:

```text
Why did revenue drop this month?
Which sellers need attention?
Which states have high late-delivery rates?
Which product categories have low review scores?
Are there unusual freight cost patterns?
Summarise the most important operational risks.
What actions should management take?
```

Design principle:

The AI assistant explains trusted data. It does not replace the warehouse or invent unsupported answers.

---

## 10. Logging and Monitoring Architecture

The project includes local logging first and Azure Monitor later.

### Local Logs

```text
logs/raw_load.log
logs/staging_load.log
logs/warehouse_load.log
logs/kpi_views.log
logs/operational_metrics.log
logs/operational_anomaly_detection.log
logs/operational_event_pipeline.log
```

Monitoring purpose:

* Track successful pipeline runs
* Track failed pipeline runs
* Store error messages
* Support debugging
* Prepare for Azure Monitor integration

---

## 11. Testing Architecture

The project will include three levels of testing.

```text
Unit Tests
   ↓
Integration Tests
   ↓
API Tests
```

Planned test areas:

| Test Type          | Purpose                                  |
| ------------------ | ---------------------------------------- |
| Unit tests         | Test individual functions                |
| Integration tests  | Test database and pipeline flow          |
| API tests          | Test FastAPI endpoints                   |
| Data quality tests | Test business rules and validation logic |

---

## 12. Docker and CI/CD Architecture

The project will use Docker and GitHub Actions.

```text
Code pushed to GitHub
      ↓
GitHub Actions Workflow
      ↓
Install dependencies
      ↓
Run tests
      ↓
Build Docker image
      ↓
Deploy later to Azure
```

Purpose:

* Demonstrate software engineering practices
* Make the project easier to run
* Support automated testing
* Prepare for cloud deployment

---

## 13. Azure Target Architecture

The final cloud version will use Azure services.

```text
Olist CSV Files
      ↓
Azure Blob Storage
      ↓
Azure Data Factory
      ↓
Azure SQL Database
      ↓
Warehouse Tables + KPI Views
      ↓
Operational Metrics + Anomaly Alerts
      ↓
Power BI
      ↓
FastAPI on Azure App Service or Container Apps
      ↓
AI Business Insights Assistant
      ↓
Azure Key Vault + Azure Monitor
```

### Azure Services

| Azure Service                      | Purpose                                                    |
| ---------------------------------- | ---------------------------------------------------------- |
| Azure Blob Storage                 | Store raw and operational event files                      |
| Azure Data Factory                 | Orchestrate ETL and event-driven pipelines                 |
| Azure SQL Database                 | Store raw, staging, warehouse, KPI, and operational tables |
| Azure App Service / Container Apps | Host FastAPI backend                                       |
| Azure Key Vault                    | Store secrets securely                                     |
| Azure Monitor                      | Monitor logs, failures, and application health             |
| Power BI                           | Executive reporting and dashboarding                       |

---

## 14. Security Architecture

The platform will include basic security features.

```text
User Login
   ↓
JWT Token
   ↓
Role-Based Access Control
   ↓
Protected API Endpoints
```

### Planned Roles

| Role    | Access                                            |
| ------- | ------------------------------------------------- |
| Admin   | Full access                                       |
| Analyst | KPI, operational anomaly, event, and AI endpoints |
| Viewer  | Read-only dashboard and summary access            |

---

## 15. End-to-End Architecture Summary

```text
Source Data
   ↓
Raw Layer
   ↓
Validation Layer
   ↓
Staging Layer
   ↓
Warehouse Layer
   ↓
KPI Layer
   ↓
Operational Metrics and Anomaly Detection
   ↓
Power BI + FastAPI
   ↓
AI Business Insights
   ↓
Azure Deployment + Monitoring
```

This architecture is designed to demonstrate practical Data Engineering, Analytics Engineering, Business Intelligence, AI integration, cloud deployment, testing, and production-style engineering practices.



## Docker Containerisation Layer

The FastAPI backend is containerised using Docker.

Docker provides a reproducible runtime environment for the API and prepares the backend for future CI/CD and Azure deployment workflows.

### Docker Architecture

```text
Dockerfile
    ↓
Docker image
    ↓
Docker container
    ↓
FastAPI backend running on port 8000
    ↓
SQLite database mounted at runtime for local demonstration
```

### Container Purpose

The Docker container runs the API serving layer of the project.

The containerised API exposes:

- Executive KPI endpoints
- Sales performance endpoints
- Operational anomaly endpoints
- Operational risk endpoints
- AI-ready business insight endpoints
- Health check endpoints

### Container Contents

The local Docker container includes:

| Component | Purpose |
|---|---|
| `src/` | FastAPI application code and supporting Python modules |
| `requirements.txt` | Python dependencies required by the API |
| `.env.example` | Example environment variables and demo API keys |
| API routes | Executive, operations, insights, and health endpoints |
| Authentication logic | API-key authentication and role-based access control |
| Logging configuration | API request logging and error logging |
| Health checks | Basic and system-level API health endpoints |

The SQLite database is not copied into the image. It is mounted at runtime from the local project folder.

### Local Docker Flow

```text
User / Browser / Swagger UI
        ↓
http://127.0.0.1:8000/docs
        ↓
Docker container
        ↓
FastAPI backend
        ↓
Mounted SQLite database
        ↓
JSON API response
```

### Local Docker Design

The local Docker version mounts the SQLite database into the container:

```text
retail_intelligence.db
```

This allows the API to run as a local demonstration without making the Docker image unnecessarily large.

This design is more professional than copying a large database into the image because it separates application code from runtime data.

### Future Azure Architecture

In the Azure version, the API will not use a local SQLite file.

Instead, the containerised API will connect to Azure SQL Database.

```text
User / Browser / API Client
        ↓
Azure-hosted FastAPI backend
        ↓
Azure SQL Database
        ↓
Curated warehouse, KPI, operational, and insight data
```

### Local and Cloud Difference

| Area | Local Docker Version | Future Azure Version |
|---|---|---|
| API hosting | Docker Desktop | Azure App Service or container hosting |
| Database | SQLite database mounted at runtime | Azure SQL Database |
| Secrets | Demo API keys for local testing | Azure Key Vault |
| Monitoring | Local logs | Azure Monitor |
| Deployment | Manual Docker commands | GitHub Actions CI/CD and Azure deployment |

### Architecture Benefit

The Docker layer demonstrates that the API can run outside the local Python virtual environment.

This improves the project architecture by adding a deployment-ready backend layer that can later be integrated with CI/CD and Azure cloud services.


## CI Pipeline Architecture

The project uses GitHub Actions to run automated CI checks when code is pushed to GitHub.

This phase implements a database-independent CI foundation because the local SQLite database is a large generated file and is not committed to GitHub.

### CI Flow

```text
Developer pushes code to GitHub
        ↓
GitHub Actions starts
        ↓
Checkout repository
        ↓
Confirm local database is not tracked
        ↓
Set up Python 3.10
        ↓
Install dependencies
        ↓
Validate Python syntax
        ↓
Validate core imports
        ↓
Verify Docker setup
        ↓
Verify CI setup
        ↓
Build Docker image
        ↓
CI result: pass or fail
```

### CI Workflow File

```text
.github/workflows/ci.yml
```

### CI Responsibilities

The CI pipeline is responsible for:

- Validating repository structure
- Confirming the large local database is not tracked
- Installing project dependencies
- Checking Python syntax
- Validating important Python imports
- Verifying Docker setup and documentation
- Verifying CI setup and documentation
- Confirming the Docker image can be built

### Database-Independent CI

The local SQLite database is not included in GitHub because it is a large generated file.

For this reason, the CI pipeline avoids tests that require `retail_intelligence.db`.

Local tests still validate the API, database-backed endpoints, RBAC rules, AI-ready insights, and pipeline outputs.

In a later Azure phase, CI can be expanded to run against Azure SQL Database or a smaller CI test database.

### CI and Future CD

This phase implements Continuous Integration only.

Continuous Deployment will be added later after the Azure hosting, database, secrets, and monitoring layers are completed.


## Azure SQL Database Serving Layer

Azure SQL Database is used as the cloud serving database for curated analytical outputs.

This layer moves the project from a local-only SQLite setup toward a managed cloud database architecture.

### Azure SQL Architecture Flow

```text
Azure Blob Storage
        ↓
Raw Olist CSV landing zone
        ↓
Python + dbt transformation pipeline
        ↓
Local SQLite curated warehouse
        ↓
Azure SQL migration script
        ↓
Azure SQL Database
        ↓
Future FastAPI / Power BI cloud serving
```

### Azure SQL Role

Azure SQL Database stores curated serving-layer tables, including:

- Dimension tables
- Fact tables
- Operational metric tables
- Anomaly detection tables
- Event pipeline tables

### Loaded Object Groups

| Group | Tables |
|---|---|
| Dimensions | `dim_date`, `dim_customer`, `dim_product`, `dim_seller` |
| Facts | `fact_sales`, `fact_delivery`, `fact_payments`, `fact_reviews` |
| Operational metrics | `ops_daily_metrics`, `ops_seller_metrics`, `ops_category_metrics` |
| Anomaly detection | `ops_anomaly_rules`, `ops_anomaly_alerts` |
| Event pipeline | `ops_event_log`, `ops_event_records` |

### Current Local-to-Cloud Design

At this stage, the local pipeline still builds the full analytical model in SQLite.

A migration script then loads selected curated objects into Azure SQL Database.

This design is intentional for the portfolio version because it allows the project to keep a working local development environment while adding a cloud serving database.

### Future Cloud Design

In later phases, the architecture can evolve into:

```text
Azure Blob Storage
        ↓
Azure Data Factory
        ↓
Azure SQL Database
        ↓
FastAPI / Power BI
```

### Architecture Benefit

Adding Azure SQL Database demonstrates that the project can publish curated analytical outputs to a managed cloud database.

This prepares the backend and reporting layers for cloud deployment and production-style access patterns.


## Azure Data Factory Orchestration Layer

Azure Data Factory is used as the cloud orchestration layer.

In this phase, ADF copies raw order data from Azure Blob Storage into Azure SQL Database.

```text
Azure Blob Storage
        ↓
ADF Copy Activity
        ↓
Azure SQL staging table
```

The implemented pipeline is:

```text
pl_copy_olist_orders_blob_to_sql
```

The pipeline reads:

```text
ecommerce-retail-data/raw/olist/olist_orders_dataset.csv
```

and writes to:

```text
dbo.adf_stg_orders_raw
```

This demonstrates cloud-based orchestration without replacing the full local Python/dbt transformation pipeline yet.

Future phases can extend this into metadata-driven ingestion and scheduled orchestration.


## Azure App Service API Deployment Layer

The platform includes a cloud-hosted FastAPI backend deployed on Azure App Service for Containers.

This layer exposes curated business metrics, operational anomaly alerts, and AI-ready insight outputs through API endpoints.

### Deployment Flow

```text
Local FastAPI source code
        ↓
Docker image
        ↓
Azure Container Registry
        ↓
Azure App Service
        ↓
Azure SQL Database
```

### Architecture Role

| Component | Role |
|---|---|
| Docker | Packages the FastAPI backend and dependencies |
| Azure Container Registry | Stores the deployable API image |
| Azure App Service | Runs the API container and exposes HTTPS endpoints |
| Azure SQL Database | Provides the deployed API data backend |
| Managed Identity | Allows secure image pull from ACR |
| Environment Variables | Configure runtime mode, SQL connection, and API keys |

### Runtime Design

The API uses an environment-driven database mode:

```text
APP_ENV=local → SQLite
APP_ENV=azure → Azure SQL Database
```

This allows the same application code to run locally and in Azure.

### Cloud API Flow

```text
User / Browser / API Client
        ↓
Azure App Service HTTPS Endpoint
        ↓
FastAPI Routes
        ↓
Authentication and RBAC
        ↓
Azure SQL Serving Tables
        ↓
JSON API Response
```

### Final Cloud Serving Architecture

```text
Azure Blob Storage
        ↓
Azure Data Factory
        ↓
Azure SQL Database
        ↓
Azure App Service FastAPI Backend
        ↓
Business users / API clients / dashboard layer
```

The Azure App Service layer completes the application-serving part of the cloud architecture.


## Azure Key Vault Security Layer

The platform uses Azure Key Vault to manage sensitive runtime configuration for the deployed FastAPI API.

### Secret Resolution Flow

```text
Azure Key Vault
        ↓
Key Vault references in App Service settings
        ↓
Azure App Service managed identity
        ↓
Resolved environment variables
        ↓
FastAPI application
```

### Role in Architecture

| Component | Responsibility |
|---|---|
| Azure Key Vault | Stores SQL credentials and API keys |
| App Service managed identity | Authenticates App Service to Key Vault |
| App Service Key Vault references | Inject secrets into runtime environment variables |
| FastAPI application | Reads resolved values as normal environment variables |
| Azure SQL Database | Receives authenticated database connection |

### Why This Matters

The application does not need to store sensitive values directly in code, Docker images, GitHub, or plain App Service settings.

This creates a cleaner separation between:

- Application code
- Deployment configuration
- Secret storage
- Runtime access control

### Updated Cloud Architecture

```text
Azure Blob Storage
        ↓
Azure Data Factory
        ↓
Azure SQL Database
        ↑
Azure Key Vault
        ↓
Azure App Service FastAPI API
        ↓
Authenticated API clients
```

### Runtime Modes

The same FastAPI codebase supports both local and cloud operation:

| Runtime | Database | Secret Handling |
|---|---|---|
| Local development | SQLite or Azure SQL | `.env` file |
| Azure deployment | Azure SQL | Key Vault references |

This allows the project to remain easy to develop locally while using stronger cloud security practices in Azure.

## Azure Monitoring and Observability Layer

The platform includes a monitoring layer for the deployed FastAPI API.

This layer helps validate that the deployed API is reachable, observable, and monitored for availability failures.

### Monitoring Architecture

```text
API Client / Browser
        ↓
Azure App Service FastAPI API
        ↓
App Service Logs and Log Stream

Application Insights
        ↓
Availability Test against /health/
        ↓
Azure Monitor Alert Rule
```

### Monitoring Components

| Component | Role |
|---|---|
| App Service Logs | Captures application/container logs |
| Log Stream | Provides live log visibility |
| Application Insights | Tracks availability and monitoring signals |
| Availability Test | Calls the public `/health/` endpoint |
| Alert Rule | Detects failed health checks across test locations |

### Availability Monitoring Flow

```text
Application Insights
        ↓
Calls /health/ every 5 minutes
        ↓
Expects HTTP 200
        ↓
Records success/failure by region
        ↓
Triggers alert if multiple locations fail
```

### Health Check Design

The API exposes a public health endpoint:

```text
/health/
```

This endpoint validates:

- FastAPI service availability
- Database connectivity status

Expected response:

```json
{
  "status": "ok",
  "service": "E-Commerce Retail Intelligence API",
  "database_connected": true
}
```

### Free Tier Design Decision

Built-in App Service Health Check was skipped because it requires a Basic B1 or higher App Service plan.

To keep the portfolio project cost-controlled, Application Insights availability testing is used instead.

### Updated Cloud Architecture

```text
Azure Blob Storage
        ↓
Azure Data Factory
        ↓
Azure SQL Database
        ↑
Azure Key Vault
        ↓
Azure App Service FastAPI API
        ↓
Application Insights Monitoring
        ↓
Azure Monitor Availability Alert
```

 ## Final Implemented Architecture Summary

The final implemented platform combines local data engineering, analytics engineering, cloud deployment, security, and monitoring.

```text
Olist CSV Data
        ↓
Python Ingestion
        ↓
SQLite Raw Tables
        ↓
Data Quality Validation
        ↓
Staging and Warehouse Models
        ↓
dbt Transformations and Tests
        ↓
Operational KPI and Anomaly Detection Layer
        ↓
Azure Blob Storage
        ↓
Azure Data Factory
        ↓
Azure SQL Database
        ↓
FastAPI Backend with Authentication and RBAC
        ↓
Docker Image
        ↓
Azure Container Registry
        ↓
Azure App Service
        ↓
Azure Key Vault
        ↓
Application Insights Monitoring
```

### Final Architecture Layers

| Layer | Technology | Purpose |
|---|---|---|
| Source data | Olist CSV files | Raw e-commerce data source |
| Local ingestion | Python, pandas, SQLite | Load raw data into local analytical database |
| Data quality | Python, SQL | Validate completeness, duplicates, nulls, dates, and relationships |
| Transformation | SQL, dbt | Build staging, warehouse, and analytical models |
| Warehouse | SQLite locally, Azure SQL in cloud | Store curated dimensions, facts, KPIs, and operational outputs |
| Operational intelligence | SQL, Python | Generate operational metrics and anomaly alerts |
| API | FastAPI | Serve curated metrics and insights as JSON |
| Security | API keys, RBAC, Azure Key Vault | Protect endpoints and secrets |
| Containerization | Docker | Package the API for deployment |
| Image registry | Azure Container Registry | Store deployable API image |
| Hosting | Azure App Service | Run the FastAPI container in Azure |
| Monitoring | App Service Logs, Application Insights | Track logs, health, and availability |

### Final Cloud Architecture

```text
Azure Blob Storage
        ↓
Azure Data Factory
        ↓
Azure SQL Database
        ↑
Azure Key Vault
        ↓
Azure App Service FastAPI API
        ↓
Application Insights Availability Test
        ↓
Azure Monitor Alert Rule
```

### Final Local Development Architecture

```text
Raw Olist CSV files
        ↓
Python ingestion scripts
        ↓
SQLite database
        ↓
dbt transformations and tests
        ↓
Operational anomaly detection
        ↓
FastAPI local API
        ↓
Automated tests
```

### Final Design Decisions

| Decision | Reason |
|---|---|
| SQLite for local development | Keeps local development simple, reproducible, and low-cost |
| Azure SQL for cloud serving | Allows the deployed API to query cloud-hosted curated data |
| Azure Blob for raw files | Provides a cloud raw data landing zone |
| Azure Data Factory for orchestration | Demonstrates Azure-native data movement |
| FastAPI for serving | Lightweight API layer for analytical outputs |
| Docker for deployment | Makes the API portable and cloud deployable |
| Azure App Service for hosting | Provides managed container hosting without Kubernetes complexity |
| Azure Key Vault for secrets | Keeps SQL credentials and API keys out of source code and plain app settings |
| Application Insights for monitoring | Provides external availability testing and alerting |
| Power BI deferred to final phase | Keeps dashboarding as the presentation layer after engineering completion |

## GitHub Actions CI/CD Architecture

The project includes separate GitHub Actions workflows for CI and CD.

| Workflow | File | Purpose |
|---|---|---|
| CI Pipeline | `.github/workflows/ci.yml` | Validates code, imports, setup checks, and Docker image build |
| CD Pipeline | `.github/workflows/cd-azure-app.yml` | Builds and deploys the FastAPI Docker image to Azure App Service |

---

### CI/CD Architecture Flow

```text
Developer pushes code to main
        ↓
GitHub Actions CI Pipeline
        ↓
Validate project structure, imports, setup checks, and Docker build
        ↓
GitHub Actions CD Pipeline
        ↓
Login to Azure using service principal
        ↓
Build Docker image
        ↓
Push Docker image to Azure Container Registry
        ↓
Ensure App Service managed identity exists
        ↓
Ensure App Service identity has AcrPull permission
        ↓
Configure managed identity based ACR image pull
        ↓
Set App Service container image
        ↓
Restart Azure App Service
        ↓
Verify deployed /health/ endpoint
```

---

### CI Pipeline Role

The CI pipeline validates that the project is buildable and structurally correct before deployment.

It checks:

- Python dependency installation
- Python syntax compilation
- Core imports
- Docker setup verification
- CI setup verification
- Docker image build
- Large database file is not tracked by Git

This provides confidence that the repository can be built in a clean GitHub Actions environment.

---

### CD Pipeline Role

The CD pipeline automates deployment to Azure App Service.

It performs:

- Azure login using a service principal
- Docker image build
- Docker image push to Azure Container Registry
- App Service managed identity validation
- `AcrPull` permission validation
- Managed identity based ACR image pull configuration
- App Service container image update
- Web App restart
- Post-deployment health check

This turns deployment from a manual Docker push process into a repeatable GitHub Actions deployment process.

---

### Container Deployment Flow

```text
GitHub Actions runner
        ↓
Docker build
        ↓
Azure Container Registry
        ↓
Azure App Service pulls image
        ↓
FastAPI container starts
        ↓
/health/ endpoint validates API and Azure SQL connectivity
```

---

### Managed Identity ACR Pull Flow

Azure App Service pulls the Docker image from Azure Container Registry using managed identity.

```text
App Service system-assigned managed identity
        ↓
AcrPull role on Azure Container Registry
        ↓
acrUseManagedIdentityCreds = true
        ↓
Secure image pull from ACR
```

This avoids storing ACR username/password credentials in App Service configuration.

---

### Post-Deployment Verification Flow

The CD workflow verifies the deployed app using the public health endpoint:

```text
/health/
```

Expected response:

```json
{
  "status": "ok",
  "service": "E-Commerce Retail Intelligence API",
  "database_connected": true
}
```

The health check confirms:

- App Service is reachable
- FastAPI container started successfully
- The API can connect to Azure SQL Database

Because the health endpoint checks Azure SQL connectivity, Azure SQL Database must be online when the CD workflow runs.

---

### CI/CD Troubleshooting Outcome

During implementation, the first CD deployment surfaced an Azure image pull issue:

```text
ImagePullUnauthorizedFailure
```

The issue was resolved by:

```text
Enabling App Service managed identity
Assigning AcrPull permission on Azure Container Registry
Setting acrUseManagedIdentityCreds=true
Updating the CD workflow to preserve managed identity based ACR pull
```

This final design is documented in:

```text
docs/azure_ci_cd.md
```

### Final Technical Documentation

For cleaner final documentation, use:

| Document | Description |
|---|---|
| `docs/final_architecture.md` | Final architecture summary |
| `docs/technical_architecture.md` | Technical design and engineering decisions |
| `docs/system_flow.md` | Data, API, deployment, security, and monitoring flows |