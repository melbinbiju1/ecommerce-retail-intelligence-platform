# Data Lineage

## Project Name

**E-Commerce Retail Intelligence Platform with Operational Anomaly Detection and AI-Ready Business Insights**

---

## Purpose

This document explains how data moves through the project from raw Olist e-commerce CSV files to curated warehouse models, operational anomaly outputs, API serving objects, AI-ready insights, and Power BI reporting outputs.

This document focuses only on **data movement and transformation lineage**. Detailed architecture, security, CI/CD, monitoring, and Azure setup are documented separately.

---

## 1. High-Level Lineage

```text
Olist CSV files
      ↓
Python raw ingestion
      ↓
Raw SQLite tables
      ↓
Raw data quality checks
      ↓
dbt staging models
      ↓
dbt warehouse models
      ↓
KPI and operational models
      ↓
Operational anomaly detection
      ↓
API serving views / Power BI export layer
      ↓
Azure SQL Database serving layer
      ↓
FastAPI analytics API
      ↓
AI-ready insights and Power BI dashboard
```

---

## 2. Source-to-Raw Lineage

The project starts with the Olist Brazilian E-Commerce Public Dataset.

| Source File | Raw Table | Purpose |
|---|---|---|
| `olist_orders_dataset.csv` | `raw_orders` | Order lifecycle and delivery timestamps |
| `olist_order_items_dataset.csv` | `raw_order_items` | Product, seller, price, and freight details at order-item level |
| `olist_order_payments_dataset.csv` | `raw_order_payments` | Payment type, value, installments, and sequence |
| `olist_order_reviews_dataset.csv` | `raw_order_reviews` | Review score and review timing |
| `olist_customers_dataset.csv` | `raw_customers` | Customer identifiers and location |
| `olist_products_dataset.csv` | `raw_products` | Product metadata and category information |
| `olist_sellers_dataset.csv` | `raw_sellers` | Seller identifiers and location |
| `product_category_name_translation.csv` | `raw_product_category_translation` | Portuguese-to-English product category mapping |
| `olist_geolocation_dataset.csv` | `raw_geolocation` | Brazilian geolocation reference data |

Lineage flow:

```text
Raw CSV files
      ↓
Python ingestion scripts
      ↓
Raw SQLite tables
```

---

## 3. Raw Data Quality Lineage

Raw tables are validated before transformation.

```text
Raw SQLite tables
      ↓
Data quality validation scripts
      ↓
Data quality reports
      ↓
Approved inputs for staging
```

Main validation areas:

| Check Type | Purpose |
|---|---|
| Row count checks | Confirm source files loaded correctly |
| Null checks | Identify missing values in important fields |
| Duplicate checks | Detect repeated IDs or duplicate records |
| Referential checks | Validate relationships across source tables |
| Date checks | Identify invalid or inconsistent timestamps |
| Numeric checks | Validate prices, freight values, payments, and review scores |

---

## 4. Raw-to-Staging Lineage

The staging layer standardises raw data for downstream modelling.

```text
Raw tables
      ↓
dbt staging models
      ↓
Cleaned and standardised staging outputs
```

The staging layer handles:

| Transformation Area | Description |
|---|---|
| Column naming | Applies consistent column names |
| Type casting | Converts dates, numeric fields, and identifiers |
| Basic cleaning | Prepares source data for modelling |
| Source alignment | Keeps staged models close to raw source meaning |
| Reusable base models | Provides clean inputs for facts, dimensions, and KPIs |

---

## 5. Staging-to-Warehouse Lineage

Staging models are transformed into dimensional warehouse outputs.

```text
Staging models
      ↓
Dimensional modelling
      ↓
Fact and dimension tables
```

| Warehouse Object | Type | Main Inputs | Purpose |
|---|---|---|---|
| `dim_date` | Dimension | Order and delivery date fields | Calendar analysis |
| `dim_customer` | Dimension | Customer staging data | Customer and geography analysis |
| `dim_product` | Dimension | Product and category staging data | Product analysis |
| `dim_seller` | Dimension | Seller staging data | Seller analysis |
| `fact_sales` | Fact | Orders, items, products, sellers, customers | Revenue and item-level sales analysis |
| `fact_delivery` | Fact | Orders and customers | Delivery timing and delay analysis |
| `fact_payments` | Fact | Order payments | Payment behaviour analysis |
| `fact_reviews` | Fact | Order reviews | Review and satisfaction analysis |

---

## 6. Warehouse-to-KPI Lineage

Warehouse facts and dimensions feed analytical KPI views.

```text
Fact and dimension tables
      ↓
KPI models and views
      ↓
Executive and operational analytics outputs
```

| KPI / Serving View | Purpose |
|---|---|
| `vw_executive_summary` | High-level order, revenue, delivery, and review metrics |
| `vw_monthly_sales` | Monthly sales and revenue performance |
| `vw_product_performance` | Product-level sales and revenue ranking |
| `vw_seller_performance` | Seller-level sales, revenue, and delivery metrics |
| `vw_customer_state_performance` | Customer geography and state-level performance |

These outputs support executive reporting, API responses, AI-ready summaries, and Power BI visuals.

---

## 7. Operational Metrics and Anomaly Lineage

Operational metrics are created from warehouse outputs and used for anomaly detection.

```text
Warehouse facts and KPI models
      ↓
Operational metric tables
      ↓
Anomaly detection rules
      ↓
Operational anomaly alerts
      ↓
Operational risk views
```

| Operational Object | Purpose |
|---|---|
| `ops_daily_metrics` | Daily operational performance metrics |
| `ops_seller_metrics` | Seller-level delivery, review, and risk metrics |
| `ops_category_metrics` | Category-level delivery and review metrics |
| `ops_anomaly_rules` | Rule definitions for anomaly detection |
| `ops_anomaly_alerts` | Generated anomaly alert records |
| `ops_event_log` | Event pipeline execution log |
| `ops_event_records` | Event-level operational alert records |

Operational serving views include:

| View | Purpose |
|---|---|
| `vw_operational_alert_summary` | Overall alert summary |
| `vw_operational_alerts_by_type` | Alert counts by type |
| `vw_operational_alerts_by_severity` | Alert counts by severity |
| `vw_recent_operational_alerts` | Recent operational alert records |
| `vw_high_risk_sellers` | Seller-level risk output |
| `vw_high_risk_categories` | Category-level risk output |
| `vw_operational_risk_summary` | Overall operational risk summary |

---

## 8. Cloud Serving Lineage

Curated local outputs are migrated to Azure SQL Database for cloud serving.

```text
Local warehouse, KPI, and anomaly outputs
      ↓
Azure SQL migration scripts
      ↓
Azure SQL Database tables and serving objects
      ↓
FastAPI deployed API
```

Azure SQL stores the curated data used by the deployed API, including:

| Layer | Examples |
|---|---|
| Dimensions | `dim_date`, `dim_customer`, `dim_product`, `dim_seller` |
| Facts | `fact_sales`, `fact_delivery`, `fact_payments`, `fact_reviews` |
| Operational tables | `ops_daily_metrics`, `ops_seller_metrics`, `ops_category_metrics` |
| Anomaly tables | `ops_anomaly_rules`, `ops_anomaly_alerts` |
| API serving views/tables | `vw_executive_summary`, `vw_operational_alert_summary`, `vw_high_risk_sellers` |

Azure Blob Storage and Azure Data Factory support the cloud ingestion/orchestration layer:

```text
Raw Olist CSV files
      ↓
Azure Blob Storage raw/olist/
      ↓
Azure Data Factory copy pipeline
      ↓
Azure SQL staging table
```

---

## 9. API and Insight Consumption Lineage

FastAPI consumes curated serving objects and exposes them through secured business endpoints.

```text
Azure SQL serving objects
      ↓
FastAPI route handlers
      ↓
JWT-protected API endpoints
      ↓
Executive, operations, and insight responses
```

| API Group | Data Consumed | Output |
|---|---|---|
| `/executive/*` | Executive KPI views | Revenue, sales, customer, seller, and product metrics |
| `/operations/*` | Operational anomaly views | Alert summaries, severity breakdowns, and risk outputs |
| `/insights/*` | KPI and operational views | AI-ready business summaries and recommendations |

Protected API endpoints require:

```text
Authorization: Bearer <access_token>
```

---

## 10. Power BI Consumption Lineage

Power BI uses curated analytical outputs from the Power BI export layer and KPI outputs.

```text
Warehouse and KPI outputs
      ↓
Power BI export layer
      ↓
Power BI dashboard
```

Planned dashboard areas:

| Dashboard Area | Data Source |
|---|---|
| Executive overview | Executive KPI outputs |
| Sales performance | Monthly sales, product, and seller outputs |
| Operational risk | Anomaly and risk views |
| Customer geography | Customer state performance outputs |
| Seller and product performance | Seller and product KPI outputs |

---

## 11. Final Lineage Summary

The final lineage shows how raw e-commerce data becomes business-ready intelligence.

```text
Raw CSV files
      ↓
Validated raw tables
      ↓
Clean staging models
      ↓
Warehouse facts and dimensions
      ↓
KPI and operational views
      ↓
Anomaly detection outputs
      ↓
Azure SQL serving layer
      ↓
JWT-protected FastAPI endpoints
      ↓
AI-ready insight responses
      ↓
Power BI dashboard
```

This lineage demonstrates the full data path from raw source files to analytical, operational, API, AI-ready, and BI-ready outputs.