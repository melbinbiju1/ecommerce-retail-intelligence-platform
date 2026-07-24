# Project Scope

## Project Name

**E-Commerce Retail Intelligence Platform**

## Project Subtitle

**End-to-End Data Engineering and AI Business Insights Platform using Olist E-Commerce Data**

## Main Goal

Build an end-to-end Data Engineering and AI platform using real e-commerce order data from the Olist Brazilian E-Commerce dataset.

The platform ingests raw data, validates quality, transforms it into a warehouse model, creates business KPI views, detects operational anomalies, and provides AI-powered business explanations and recommendations.

## Primary Focus

**Data Engineering**

## Secondary Focus

**AI / Generative AI for Business Insights**

## Supporting Focus

**Business Intelligence and Analytics**

---

## Business Problem

E-commerce companies need a reliable way to monitor sales performance, delivery performance, seller behaviour, payment patterns, customer satisfaction, and operational risks.

Without a proper data platform, business teams may struggle to answer questions such as:

* Is revenue increasing or decreasing?
* Which sellers are underperforming?
* Which product categories generate the most revenue?
* Are deliveries becoming slower?
* Are customers giving lower review scores?
* Are freight costs unusually high?
* Are cancellations increasing?
* What are the most important operational risks this week or month?

This project solves the problem by building a centralised analytics and AI insight platform.

---

## Dataset

The project uses the **Olist Brazilian E-Commerce Public Dataset** as the real core dataset.

The dataset includes:

* Orders
* Order items
* Customers
* Products
* Sellers
* Payments
* Reviews
* Delivery timestamps
* Geolocation
* Product category translation

This dataset is suitable for building realistic e-commerce analytics, data engineering pipelines, warehouse models, operational KPI views, delivery analysis, seller performance analysis, review analysis, and AI business insights.

---

## Main Platform Features

### Data Engineering Features

* Data ingestion from CSV files
* Raw data layer
* Raw file inspection
* Raw database loading
* Raw data quality validation
* Staging layer
* Warehouse star schema
* KPI SQL views
* Logging
* Error handling
* Pipeline verification reports

### Operational Analytics Features

* Revenue analysis
* Monthly sales analysis
* Product category performance
* Seller performance
* Customer state performance
* Delivery performance
* Payment analysis
* Review analysis
* Freight cost analysis
* Cancellation analysis

### Operational Anomaly Detection Features

The project detects operational anomalies using real Olist business data.

Planned anomaly areas:

* Revenue drop anomalies
* Order volume spike anomalies
* Delivery delay anomalies
* Seller performance anomalies
* Payment anomalies
* Freight cost anomalies
* Review score anomalies
* Cancellation anomalies
* Product category performance anomalies

### Event-Driven Pipeline Feature

The project includes an event-driven operational alert pipeline.

Local version:

```text
New operational event file arrives
      ↓
File is placed in data/operational_events/incoming
      ↓
Pipeline validates file and records
      ↓
Valid events are loaded into the database
      ↓
Invalid events are stored with failure reasons
      ↓
File is moved to processed or failed folder
      ↓
Event log is updated
```

Azure version:

```text
New file uploaded to Azure Blob Storage
      ↓
Azure Data Factory trigger runs
      ↓
Pipeline validates and loads event data
      ↓
Azure SQL Database is updated
      ↓
Power BI, FastAPI, and AI assistant use updated data
```

### AI Business Insights Features

The AI assistant will explain business performance and risks using trusted KPI and anomaly data.

Example questions:

* Why did revenue drop this month?
* Which sellers need attention?
* Which states have high late-delivery rates?
* Which product categories have low review scores?
* Are there unusual freight cost patterns?
* What are the main operational risks?
* What actions should management take?

### Power BI Features

The Power BI dashboard will include:

* Executive overview
* Sales performance
* Product category performance
* Seller performance
* Customer geography
* Delivery performance
* Payment analysis
* Review analysis
* Operational anomaly alerts
* AI business insights summary

### API Features

FastAPI will expose secure endpoints for:

* Executive KPIs
* Monthly sales
* Product performance
* Seller performance
* Delivery performance
* Review analysis
* Operational anomalies
* Operational events
* AI business insights

### Security Features

* JWT authentication
* Role-based access control
* Admin, analyst, and viewer roles
* Protected API endpoints
* Environment-based secrets

### Cloud Features

Planned Azure services:

* Azure Blob Storage
* Azure SQL Database
* Azure Data Factory
* Azure App Service or Azure Container Apps
* Azure Key Vault
* Azure Monitor
* Power BI

### DevOps and Testing Features

* Docker
* GitHub Actions
* Unit tests
* Integration tests
* API tests
* Health check endpoint
* Structured logging
* Error handling
* Monitoring-ready logs

---

## Out of Scope

This project does not aim to build a full production marketplace system.

The following are outside the current scope:

* Real-time payment processing
* Real customer authentication system
* Full marketplace backend
* Production-level recommendation engine
* Advanced deep learning forecasting
* Live connection to Olist systems

