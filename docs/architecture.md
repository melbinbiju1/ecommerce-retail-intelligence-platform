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

---

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