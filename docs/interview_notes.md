# Interview Notes

## Project Name

**E-Commerce Retail Intelligence Platform**

## One-Line Explanation

This is an end-to-end Data Engineering and AI Business Insights platform built using the Olist Brazilian E-Commerce dataset. It ingests raw e-commerce data, validates quality, transforms it into a warehouse model, creates KPI views, detects operational anomalies, and uses AI to explain business risks and recommendations.

---

## 1. How to Explain the Project

I built this project to simulate how an e-commerce company can turn raw marketplace data into trusted business insights.

The platform takes raw Olist CSV files, loads them into a raw database layer, validates data quality, transforms the data into staging tables, builds a warehouse star schema, creates KPI views, detects operational anomalies, and prepares the data for Power BI, FastAPI, and AI-powered business insights.

The project is mainly focused on Data Engineering, but it also includes Business Intelligence, operational analytics, API development, AI integration, and cloud deployment planning.

---

## 2. Why I Chose the Olist Dataset

I chose the Olist Brazilian E-Commerce dataset because it is a realistic multi-table e-commerce dataset.

It includes:

* Orders
* Customers
* Products
* Sellers
* Payments
* Reviews
* Delivery timestamps
* Geolocation
* Product category translation

This made it suitable for building a real data pipeline, relational modelling, warehouse design, KPI views, delivery analysis, seller performance analysis, review analysis, and operational anomaly detection.

---

## 3. Business Problem

E-commerce companies need reliable visibility into sales, seller performance, delivery delays, customer satisfaction, payment patterns, freight costs, and operational risks.

Without a trusted data platform, business teams may struggle to identify:

* Revenue drops
* Delivery delay spikes
* Poor seller performance
* High freight costs
* Low review patterns
* Cancellation spikes
* Product category performance issues

This project solves that by creating a central platform for operational reporting and AI-assisted decision-making.

---

## 4. End-to-End Data Flow

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
Power BI / FastAPI / AI Assistant
```

---

## 5. Why I Used Raw, Staging, Warehouse, and KPI Layers

I used a layered data architecture to make the project closer to a real-world data platform.

### Raw Layer

The raw layer stores the original source data with minimal changes. This supports auditability and reprocessing.

### Staging Layer

The staging layer cleans and standardises data. For example, I converted date fields, standardised text values, translated product categories, created delivery flags, and prepared data for modelling.

### Warehouse Layer

The warehouse layer stores business-ready fact and dimension tables. This makes the data easier to analyse and report.

### KPI Layer

The KPI layer contains trusted SQL views used by Power BI, FastAPI, and the AI assistant. This avoids repeated business logic across multiple tools.

---

## 6. Warehouse Design

The warehouse uses a star schema.

Main dimensions:

* `dim_date`
* `dim_customer`
* `dim_product`
* `dim_seller`

Main facts:

* `fact_sales`
* `fact_delivery`
* `fact_payments`
* `fact_reviews`

The main fact table is `fact_sales`, and its grain is one row per order item.

This design supports analysis by time, customer location, product category, seller, payment type, delivery status, and review score.

---

## 7. Data Quality Validation

I added data quality checks before creating the staging and warehouse layers.

Examples of checks:

* Missing primary keys
* Duplicate IDs
* Invalid foreign key relationships
* Negative prices
* Negative freight values
* Negative payment values
* Invalid delivery dates
* Delivered orders with missing delivery date
* Review scores outside the valid range

This shows that the pipeline does not blindly load data. It validates whether the raw data is reliable before building business outputs.

---

## 8. Operational Anomaly Detection

The project includes an operational anomaly detection layer to identify unusual patterns in real e-commerce business activity.

The anomaly detection focuses on areas that are directly supported by the Olist dataset, including sales performance, order activity, delivery timelines, seller behaviour, payment values, freight costs, customer reviews, cancellations, and product category performance.

The planned operational anomaly detection layer identifies:

* Revenue drops
* Order volume spikes
* Delivery delay spikes
* Seller performance risks
* Payment value anomalies
* Freight cost spikes
* Low review score patterns
* Cancellation spikes
* Product category revenue drops

This approach keeps the anomaly detection realistic, business-focused, and closely aligned with the available dataset.


---

## 9. Event-Driven Operational Alert Pipeline

The project includes an event-driven operational alert pipeline.

In the local version, a new operational event file is placed in:

```text
data/operational_events/incoming
```

The pipeline then:

1. Detects the file
2. Validates the schema
3. Validates each record
4. Loads valid records into `ops_event_records`
5. Stores invalid records in `ops_event_failed_records`
6. Moves the file to the processed or failed folder
7. Updates `ops_event_log`

In Azure, this pattern can be implemented using Azure Blob Storage event triggers and Azure Data Factory.

---

## 10. Why I Chose Operational Anomaly Detection

I chose operational anomaly detection because the Olist dataset naturally supports analysis of real e-commerce operations.

The dataset includes order activity, delivery timelines, seller information, payment values, freight costs, customer reviews, cancellations, and product category performance. These areas are important for an e-commerce business because they directly affect revenue, customer satisfaction, seller reliability, and operational efficiency.

Operational anomaly detection allows the platform to identify unusual business patterns such as revenue drops, late delivery spikes, poor seller performance, high freight costs, low review scores, and cancellation increases.

This makes the anomaly detection layer realistic, business-focused, and directly connected to the available dataset.

---

## 11. Power BI Dashboard Plan

The Power BI dashboard will include:

* Executive overview
* Monthly sales performance
* Product category performance
* Seller performance
* Customer geography
* Delivery performance
* Payment analysis
* Review analysis
* Operational anomaly alerts
* AI business insights summary

The goal is to build a dashboard that supports executive decision-making, not just visualise random charts.

---

## 12. FastAPI Plan

The FastAPI backend will expose secure endpoints for business KPIs and operational insights.

Planned endpoints:

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

The API layer demonstrates backend engineering, authentication, role-based access control, and AI integration.

---

## 13. AI Business Insights Assistant

The AI assistant will explain trusted KPI and anomaly data.

Example questions it can answer:

* Why did revenue drop this month?
* Which sellers need attention?
* Which states have high late-delivery rates?
* Which product categories have low review scores?
* Are there unusual freight cost patterns?
* What are the main operational risks?
* What actions should management take?

The AI assistant will not use raw data directly. It will use structured context from KPI views, operational metrics, and anomaly alerts.

This makes the AI feature safer and more business-focused.

---

## 14. Cloud Deployment Plan

The local project will later be adapted to Azure.

Planned Azure services:

| Azure Service                       | Purpose                                                    |
| ----------------------------------- | ---------------------------------------------------------- |
| Azure Blob Storage                  | Store raw files and operational event files                |
| Azure Data Factory                  | Orchestrate ETL and event-driven pipelines                 |
| Azure SQL Database                  | Store raw, staging, warehouse, KPI, and operational tables |
| Azure App Service or Container Apps | Host FastAPI backend                                       |
| Azure Key Vault                     | Store secrets securely                                     |
| Azure Monitor                       | Monitor logs and failures                                  |
| Power BI                            | Executive dashboard                                        |

---

## 15. Docker and CI/CD Plan

The project will use Docker and GitHub Actions.

Docker will make the application easier to run in different environments.

GitHub Actions will run automated checks such as:

* Dependency installation
* Unit tests
* Integration tests
* API tests

This demonstrates production-style engineering practice.

---

## 16. How to Explain the Project in a CV

Possible CV bullet:

> Built an end-to-end e-commerce data engineering platform using Python, SQL, SQLite, and the Olist dataset, implementing raw ingestion, data quality validation, staging transformations, warehouse star schema, KPI views, operational anomaly detection, and AI-ready business insight layers.

Another stronger version after Azure deployment:

> Developed an Azure-based e-commerce intelligence platform using Azure Blob Storage, Azure SQL Database, Azure Data Factory, FastAPI, Power BI, Docker, and GitHub Actions, enabling KPI reporting, operational anomaly detection, and AI-powered business insights from Olist marketplace data.

---

## 17. Possible Interview Questions and Answers

### Q1. Why did you create staging tables?

Staging tables separate cleaned data from raw data. Raw tables preserve the original source, while staging tables standardise formats, clean values, convert dates, add flags, and prepare the data for warehouse modelling.

### Q2. Why did you use a warehouse star schema?

A star schema makes reporting easier and more efficient. It separates descriptive entities such as customers, products, sellers, and dates from measurable business events such as sales, payments, delivery, and reviews.

### Q3. Why did you create KPI views?

KPI views centralise business logic. Instead of calculating metrics separately in Power BI, API code, and AI prompts, I created trusted SQL views that can be reused by all downstream layers.

### Q4. What data quality checks did you implement?

I implemented checks for missing IDs, duplicate keys, invalid foreign keys, negative prices, negative freight values, negative payments, invalid dates, missing delivery dates, and invalid review scores.

### Q5. How does the event-driven pipeline work?

A new operational event file is placed into an incoming folder. The pipeline validates the file, loads valid records, stores failed records with reasons, moves the file to processed or failed, and logs the result. In Azure, the same pattern can be implemented with Blob Storage triggers and Azure Data Factory.

### Q6. How will the AI assistant work?

The AI assistant will receive structured KPI and anomaly context from trusted database views and tables. It will generate business explanations and recommendations based on that context instead of directly querying raw data.

### Q7. What would you improve in a production version?

In production, I would use Azure SQL instead of SQLite, Azure Blob Storage for files, Azure Data Factory for orchestration, Key Vault for secrets, Azure Monitor for logs, stronger authentication, automated deployments, and more advanced anomaly detection models.

---

## 18. Final Positioning

This project should be positioned as:

**A Data Engineering and AI Business Insights platform for e-commerce operations.**

It demonstrates:

* Data ingestion
* Data quality validation
* SQL transformation
* Data warehousing
* KPI modelling
* Operational anomaly detection
* Event-driven processing
* Power BI reporting
* FastAPI backend development
* AI business insights
* Cloud deployment planning
* Testing, logging, monitoring, Docker, and CI/CD


## GitHub Actions CI Pipeline

I implemented a GitHub Actions CI pipeline to automatically validate the project when code is pushed to GitHub.

The CI pipeline installs dependencies, validates Python syntax, checks core imports, verifies Docker setup, verifies CI documentation, confirms the large local SQLite database is not tracked, and builds the Docker image.

Because the local SQLite database is a large generated artifact, it is not committed to GitHub. The CI pipeline is currently database-independent, while full database-backed tests are run locally. In a later cloud phase, CI can be expanded to run against Azure SQL Database or a smaller CI test database.

This gives the project a professional CI foundation before adding full Azure continuous deployment.


## Azure App Service Deployment Interview Notes

### Simple Explanation

I deployed the FastAPI backend as a Docker container on Azure App Service. The Docker image is stored in Azure Container Registry, and the App Service pulls the image using managed identity. The deployed API runs in Azure SQL mode, so it connects to Azure SQL Database instead of the local SQLite database.

### Technical Explanation

The application is packaged into a Docker image with the required Python dependencies and Microsoft ODBC Driver 18 for SQL Server. I pushed the image to Azure Container Registry and configured Azure App Service for Containers to run the image on port 8000. Runtime configuration is handled through App Service environment variables, including `APP_ENV=azure`, Azure SQL connection settings, and API keys. The App Service uses system-assigned managed identity with the `AcrPull` role to securely pull the container image from ACR.

### Key Skills Demonstrated

- Docker containerization
- Azure Container Registry
- Azure App Service for Containers
- Managed identity
- Azure SQL Database connectivity
- FastAPI deployment
- API authentication
- Cloud runtime configuration
- Deployment verification

## Azure Key Vault Interview Notes

### Simple Explanation

I added Azure Key Vault to manage sensitive values for the deployed API. Instead of storing SQL credentials and API keys directly in App Service settings, I stored them in Key Vault and used Key Vault references. The App Service uses managed identity to read those secrets securely.

### Technical Explanation

The Key Vault uses Azure RBAC. My developer account has the Key Vault Secrets Officer role so I can create and manage secrets. The App Service has a system-assigned managed identity with the Key Vault Secrets User role. App Service application settings use `@Microsoft.KeyVault(...)` references for SQL credentials and API keys. At runtime, App Service resolves the references and exposes the values as environment variables to the FastAPI container.

### Skills Demonstrated

- Azure Key Vault
- Secret management
- Managed identity
- Azure RBAC
- App Service Key Vault references
- Secure runtime configuration
- Cloud deployment hardening


## Azure Monitoring Interview Notes

### Simple Explanation

I added monitoring for the deployed FastAPI API using Azure App Service logs and Application Insights. I enabled Log Stream for live troubleshooting and created an availability test that checks the `/health/` endpoint every 5 minutes. An alert rule monitors availability failures across multiple test locations.

### Technical Explanation

The API runs as a container on Azure App Service. I enabled file-system application logging and verified runtime logs through Log Stream. Since App Service built-in Health Check requires Basic B1 or higher, I kept the app on the Free plan and used Application Insights Standard availability testing instead. The availability test calls the public `/health/` endpoint and expects HTTP 200. Azure automatically created an alert rule that triggers when multiple availability test locations fail.

### Skills Demonstrated

- Azure App Service logging
- Log Stream troubleshooting
- Application Insights
- Availability testing
- Azure Monitor alerts
- Cost-aware monitoring design
- Cloud operations documentation
