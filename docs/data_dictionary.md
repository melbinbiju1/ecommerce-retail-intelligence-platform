# Data Dictionary

## Project Name

**E-Commerce Retail Intelligence Platform**

## Dataset

This project uses the **Olist Brazilian E-Commerce Public Dataset** as the core transactional dataset.

The dataset contains anonymised e-commerce data including orders, customers, products, sellers, payments, reviews, delivery timestamps, geolocation, and product category translations.

---

## 1. Source Files

| File Name                               | Description                                                                               |
| --------------------------------------- | ----------------------------------------------------------------------------------------- |
| `olist_customers_dataset.csv`           | Customer identifiers and customer location information                                    |
| `olist_geolocation_dataset.csv`         | Brazilian zip-code prefix geolocation data                                                |
| `olist_order_items_dataset.csv`         | Product-level order item records including sellers, prices, and freight values            |
| `olist_order_payments_dataset.csv`      | Payment method, installments, and payment value information                               |
| `olist_order_reviews_dataset.csv`       | Customer review scores and review comments                                                |
| `olist_orders_dataset.csv`              | Order lifecycle data including purchase, approval, delivery, and estimated delivery dates |
| `olist_products_dataset.csv`            | Product category and product physical attributes                                          |
| `olist_sellers_dataset.csv`             | Seller location information                                                               |
| `product_category_name_translation.csv` | Portuguese-to-English product category translation mapping                                |

---

## 2. Generated Validation Reports

| Report                                    | Description                                                                                                                        |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `raw_file_inspection_report.csv`          | File-level validation summary including file existence, row counts, column counts, missing columns, duplicates, and missing values |
| `raw_column_profile_report.csv`           | Column-level profiling report including data types, missing values, unique values, and sample values                               |
| `raw_database_verification_report.csv`    | Verifies whether raw database tables were created successfully                                                                     |
| `raw_data_quality_results.csv`            | Stores results of raw database quality checks                                                                                      |
| `staging_table_verification_report.csv`   | Verifies whether staging tables were created successfully                                                                          |
| `warehouse_table_verification_report.csv` | Verifies whether warehouse tables were created successfully                                                                        |
| `kpi_views_verification_report.csv`       | Verifies whether KPI views were created successfully                                                                               |

---

## 3. Raw Database Tables

The raw layer stores the original Olist data with minimal transformation. Metadata columns such as `_source_file` and `_loaded_at` are added during ingestion for traceability.

| Raw Table                          | Source File                             |
| ---------------------------------- | --------------------------------------- |
| `raw_customers`                    | `olist_customers_dataset.csv`           |
| `raw_geolocation`                  | `olist_geolocation_dataset.csv`         |
| `raw_order_items`                  | `olist_order_items_dataset.csv`         |
| `raw_order_payments`               | `olist_order_payments_dataset.csv`      |
| `raw_order_reviews`                | `olist_order_reviews_dataset.csv`       |
| `raw_orders`                       | `olist_orders_dataset.csv`              |
| `raw_products`                     | `olist_products_dataset.csv`            |
| `raw_sellers`                      | `olist_sellers_dataset.csv`             |
| `raw_product_category_translation` | `product_category_name_translation.csv` |

---

## 4. Raw Load Audit

The table `raw_load_audit` records each raw file load.

| Column          | Description                               |
| --------------- | ----------------------------------------- |
| `audit_id`      | Unique audit record identifier            |
| `file_name`     | Name of the source file                   |
| `table_name`    | Target raw table                          |
| `row_count`     | Number of rows loaded                     |
| `load_status`   | Load status such as `SUCCESS` or `FAILED` |
| `error_message` | Error details if the load failed          |
| `loaded_at`     | Timestamp when the load was executed      |

---

## 5. Raw Data Quality Checks

The project includes automated raw data quality validation before building staging and warehouse tables.

### Quality Checks Implemented

* Primary key null checks
* Duplicate key checks
* Foreign key relationship checks
* Negative price checks
* Negative freight checks
* Negative payment value checks
* Invalid delivery date checks
* Missing delivery date checks for delivered orders
* Review score range checks

### Output

The results are stored in:

| Output                                        | Description                                     |
| --------------------------------------------- | ----------------------------------------------- |
| `raw_data_quality_results`                    | Database table containing quality check results |
| `data/processed/raw_data_quality_results.csv` | CSV report containing quality check results     |

These checks help prevent invalid raw data from silently entering the staging, warehouse, KPI, dashboard, API, and AI layers.

---

## 6. Staging Tables

The staging layer stores cleaned and standardised versions of the raw Olist data.

| Staging Table                      | Description                                            |
| ---------------------------------- | ------------------------------------------------------ |
| `stg_customers`                    | Cleaned customer identifiers and location fields       |
| `stg_geolocation`                  | Deduplicated zip-code geolocation reference data       |
| `stg_order_items`                  | Cleaned product-level order item records               |
| `stg_order_payments`               | Cleaned payment records                                |
| `stg_order_reviews`                | Cleaned review score and review comment indicators     |
| `stg_orders`                       | Cleaned order lifecycle data with delivery flags       |
| `stg_products`                     | Cleaned product attributes with English category names |
| `stg_sellers`                      | Cleaned seller location data                           |
| `stg_product_category_translation` | Product category translation mapping                   |

### Important Staging Transformations

* Converted text date fields into datetime format
* Standardised city names to lowercase
* Standardised state codes to uppercase
* Translated product categories into English
* Created delivery flags such as `is_delivered`, `is_late_delivery`, and `has_missing_delivery_date`
* Created `delivery_days`
* Created `item_total_value`
* Deduplicated geolocation records by zip-code prefix, city, and state
* Created review comment flag `has_review_comment`

---

## 7. Warehouse Tables

The warehouse layer stores business-ready dimension and fact tables. These tables are designed for Power BI dashboards, API endpoints, KPI views, operational anomaly detection, and AI business insight generation.

### Dimension Tables

| Warehouse Table | Description                                             |
| --------------- | ------------------------------------------------------- |
| `dim_date`      | Calendar dimension used for time-based reporting        |
| `dim_customer`  | Customer dimension with customer location information   |
| `dim_product`   | Product dimension with category and physical attributes |
| `dim_seller`    | Seller dimension with seller location information       |

### Fact Tables

| Warehouse Table | Description                                        |
| --------------- | -------------------------------------------------- |
| `fact_sales`    | Product-level sales fact table at order-item grain |
| `fact_delivery` | Order-level delivery performance fact table        |
| `fact_payments` | Payment transaction fact table                     |
| `fact_reviews`  | Customer review fact table                         |

### Warehouse Modelling Notes

* `fact_sales` is the main business fact table.
* The grain of `fact_sales` is one row per order item.
* `fact_delivery` supports delivery delay and logistics analysis.
* `fact_payments` supports payment method and installment analysis.
* `fact_reviews` supports customer satisfaction analysis.
* Surrogate keys are created for dimensions.
* `dim_date` supports reporting by day, month, quarter, and year.

---

## 8. KPI Views

The KPI layer contains business-ready SQL views used by Power BI, FastAPI endpoints, and the AI business insights assistant.

| KPI View                         | Description                                                        |
| -------------------------------- | ------------------------------------------------------------------ |
| `vw_executive_summary`           | Overall revenue, orders, item count, freight, and delivery summary |
| `vw_monthly_sales`               | Monthly sales trend by year and month                              |
| `vw_product_performance`         | Product category revenue and item performance                      |
| `vw_seller_performance`          | Seller revenue, order volume, and late delivery summary            |
| `vw_customer_state_performance`  | Revenue and order performance by customer state                    |
| `vw_delivery_performance`        | Delivery status, late delivery, and delivery duration metrics      |
| `vw_payment_analysis`            | Payment method, installment, and payment value analysis            |
| `vw_review_analysis`             | Review score distribution and delivery relationship                |
| `vw_late_delivery_by_state`      | Late delivery percentage by customer state                         |
| `vw_category_review_performance` | Product category revenue combined with review scores               |

These views form the reporting layer for executive dashboards and business insight generation.

---

## 9. Operational Metrics Layer

The operational metrics layer will generate business-level metrics from warehouse and KPI data.

Planned table:

| Table                  | Description                                            |
| ---------------------- | ------------------------------------------------------ |
| `ops_daily_metrics`    | Daily operational metrics used for anomaly detection   |
| `ops_seller_metrics`   | Seller-level operational performance metrics           |
| `ops_category_metrics` | Product category-level operational performance metrics |

### Example Metrics

| Metric                | Description                         |
| --------------------- | ----------------------------------- |
| `total_orders`        | Number of orders for the period     |
| `total_revenue`       | Total sales value                   |
| `avg_order_value`     | Average order value                 |
| `late_delivery_count` | Number of late deliveries           |
| `late_delivery_rate`  | Percentage of late deliveries       |
| `cancelled_orders`    | Number of cancelled orders          |
| `avg_review_score`    | Average customer review score       |
| `low_review_count`    | Number of 1-star and 2-star reviews |
| `avg_freight_value`   | Average freight cost                |
| `seller_count`        | Number of active sellers            |

---

## 10. Operational Anomaly Detection Layer

The operational anomaly detection layer identifies unusual business behaviour from real Olist data.

Planned table:

| Table                | Description                                                   |
| -------------------- | ------------------------------------------------------------- |
| `ops_anomaly_alerts` | Stores detected operational anomalies and recommended actions |
| `ops_anomaly_rules`  | Stores anomaly detection rule definitions                     |

### Planned Anomaly Types

| Anomaly Type              | Description                                               |
| ------------------------- | --------------------------------------------------------- |
| `REVENUE_DROP`            | Revenue is significantly below expected level             |
| `ORDER_VOLUME_SPIKE`      | Order volume is unusually high                            |
| `DELIVERY_DELAY_SPIKE`    | Late delivery rate is unusually high                      |
| `SELLER_PERFORMANCE_RISK` | Seller shows unusually poor delivery or sales performance |
| `PAYMENT_VALUE_ANOMALY`   | Payment value is unusually high or low                    |
| `FREIGHT_COST_SPIKE`      | Freight cost is significantly higher than expected        |
| `LOW_REVIEW_SPIKE`        | Low customer review scores increase unusually             |
| `CANCELLATION_SPIKE`      | Cancelled orders increase unusually                       |
| `CATEGORY_REVENUE_DROP`   | Product category revenue falls below expected level       |

### Planned Alert Fields

| Field                   | Description                                           |
| ----------------------- | ----------------------------------------------------- |
| `alert_id`              | Unique alert identifier                               |
| `alert_date`            | Date of the alert                                     |
| `alert_type`            | Type of operational anomaly                           |
| `severity`              | Alert severity such as low, medium, high, or critical |
| `business_area`         | Business area affected                                |
| `metric_name`           | Metric that triggered the alert                       |
| `actual_value`          | Actual observed value                                 |
| `expected_value`        | Expected or baseline value                            |
| `difference_value`      | Difference between actual and expected value          |
| `difference_percentage` | Percentage difference from expected value             |
| `alert_description`     | Business-friendly explanation of the alert            |
| `recommended_action`    | Suggested business action                             |
| `created_at`            | Alert creation timestamp                              |

---

## 11. Event-Driven Operational Alert Pipeline

The project includes a local event-driven operational alert pipeline that simulates processing new operational event files.

### Local Event Flow

1. A new operational event CSV file is placed in `data/operational_events/incoming`.
2. The pipeline detects the file.
3. The pipeline validates the schema and records.
4. Valid records are inserted into `ops_event_records`.
5. Invalid records are inserted into `ops_event_failed_records`.
6. The file is moved to `data/operational_events/processed` or `data/operational_events/failed`.
7. Processing details are stored in `ops_event_log`.

### Event Tables

| Table                      | Description                                    |
| -------------------------- | ---------------------------------------------- |
| `ops_event_log`            | File-level processing status and record counts |
| `ops_event_records`        | Valid operational event records                |
| `ops_event_failed_records` | Invalid records with failure reasons           |

### Supported Operational Event Types

| Event Type             | Description                                   |
| ---------------------- | --------------------------------------------- |
| `LATE_DELIVERY`        | Event related to late delivery                |
| `PAYMENT_FAILURE`      | Event related to payment failure              |
| `LOW_REVIEW`           | Event related to low review score             |
| `ORDER_CANCELLED`      | Event related to cancelled order              |
| `HIGH_FREIGHT_COST`    | Event related to unusually high freight value |
| `SELLER_DELAY_RISK`    | Event related to seller delivery risk         |
| `REVENUE_DROP`         | Event related to revenue decline              |
| `CATEGORY_DEMAND_DROP` | Event related to reduced category demand      |

### Azure Equivalent

In Azure, this local event-driven pattern can be implemented using Azure Blob Storage event triggers and Azure Data Factory pipelines. When a new file is uploaded to Blob Storage, Azure Data Factory can automatically run the ingestion and validation pipeline.

---

## 12. AI Business Insights Data Sources

The AI assistant will use trusted outputs from:

* KPI views
* Operational metrics tables
* Operational anomaly alert tables
* Event-driven operational alert tables

The AI assistant will not use raw data directly. It will explain trusted business metrics and detected anomalies.





-----------------------------------


## Operational Metrics Tables

The operational metrics layer stores business-level metrics derived from the warehouse and KPI layers. These tables are used for operational anomaly detection, Power BI reporting, FastAPI endpoints, and AI business insights.

| Table | Description |
|---|---|
| `ops_daily_metrics` | Daily sales, delivery, cancellation, review, and freight performance metrics |
| `ops_seller_metrics` | Seller-level operational performance metrics |
| `ops_category_metrics` | Product category-level operational performance metrics |

### `ops_daily_metrics`

| Column | Description |
|---|---|
| `metric_date` | Business date |
| `total_orders` | Number of orders on the date |
| `total_order_items` | Number of order item rows |
| `total_revenue` | Total item value including freight |
| `product_revenue` | Product sales value |
| `freight_revenue` | Freight value |
| `avg_order_value` | Average order value |
| `delivered_orders` | Number of delivered orders |
| `late_delivery_orders` | Number of late deliveries |
| `late_delivery_rate` | Percentage of late deliveries |
| `cancelled_orders` | Number of cancelled orders |
| `cancelled_order_rate` | Percentage of cancelled orders |
| `avg_delivery_days` | Average delivery duration |
| `total_reviews` | Number of reviews |
| `avg_review_score` | Average review score |
| `low_review_count` | Number of 1-star and 2-star reviews |
| `low_review_rate` | Percentage of low reviews |
| `created_at` | Table creation timestamp |

### `ops_seller_metrics`

Seller-level table used to identify seller performance risks based on revenue, delivery delay patterns, and review scores.

### `ops_category_metrics`

Product-category-level table used to identify category performance risks based on revenue, delivery delay patterns, and review scores.

## Operational Anomaly Detection Tables

The operational anomaly detection layer identifies unusual business patterns from the operational metrics layer.

| Table | Description |
|---|---|
| `ops_anomaly_rules` | Stores anomaly detection rule definitions |
| `ops_anomaly_alerts` | Stores detected operational anomaly alerts and recommended actions |

### `ops_anomaly_rules`

| Column | Description |
|---|---|
| `rule_id` | Unique rule identifier |
| `rule_name` | Name of the anomaly rule |
| `business_area` | Business area monitored by the rule |
| `metric_name` | Metric used by the rule |
| `rule_description` | Explanation of the rule |
| `severity` | Default severity of the rule |
| `is_active` | Indicates whether the rule is active |
| `created_at` | Rule creation timestamp |

### `ops_anomaly_alerts`

| Column | Description |
|---|---|
| `alert_id` | Unique alert identifier |
| `alert_date` | Date related to the alert |
| `alert_type` | Type of anomaly detected |
| `severity` | Alert severity |
| `business_area` | Business area affected |
| `entity_id` | Optional affected entity ID, such as seller or category |
| `entity_name` | Optional affected entity name |
| `metric_name` | Metric that triggered the alert |
| `actual_value` | Observed value |
| `expected_value` | Baseline or threshold value |
| `difference_value` | Difference between actual and expected |
| `difference_percentage` | Percentage difference between actual and expected |
| `alert_description` | Business explanation of the alert |
| `recommended_action` | Suggested business action |
| `created_at` | Alert creation timestamp |

### Anomaly Types

- `REVENUE_DROP`
- `ORDER_VOLUME_SPIKE`
- `DELIVERY_DELAY_SPIKE`
- `CANCELLATION_SPIKE`
- `LOW_REVIEW_SPIKE`
- `FREIGHT_COST_SPIKE`
- `SELLER_PERFORMANCE_RISK`
- `CATEGORY_PERFORMANCE_RISK`

## Event-Driven Operational Alert Pipeline Tables

The event-driven operational alert pipeline simulates how new operational event files are processed when they arrive.

| Table | Description |
|---|---|
| `ops_event_log` | File-level processing log for operational event files |
| `ops_event_records` | Valid operational event records |
| `ops_event_failed_records` | Invalid operational event records with failure reasons |

### Local Event Flow

1. A new operational event CSV file is placed in `data/operational_events/incoming`.
2. The pipeline validates the file schema.
3. The pipeline validates individual records.
4. Valid records are inserted into `ops_event_records`.
5. Invalid records are inserted into `ops_event_failed_records`.
6. The file is moved to `data/operational_events/processed` or `data/operational_events/failed`.
7. Processing status is stored in `ops_event_log`.

### Supported Event Types

- `LATE_DELIVERY`
- `PAYMENT_FAILURE`
- `LOW_REVIEW`
- `ORDER_CANCELLED`
- `HIGH_FREIGHT_COST`
- `SELLER_DELAY_RISK`
- `REVENUE_DROP`
- `CATEGORY_DEMAND_DROP`

### Azure Equivalent

In Azure, this local file-arrival pattern can be implemented using Azure Blob Storage event triggers and Azure Data Factory pipelines.

## Extended Operational KPI Views

The extended operational KPI views provide business-ready summaries of anomaly alerts, operational risks, and event-driven pipeline outputs.

| View | Description |
|---|---|
| `vw_operational_alert_summary` | Overall count of operational anomaly alerts by severity |
| `vw_operational_alerts_by_type` | Alert counts grouped by alert type, business area, and severity |
| `vw_operational_alerts_by_severity` | Alert distribution by severity |
| `vw_recent_operational_alerts` | Detailed operational alert records ordered by severity |
| `vw_high_risk_sellers` | Sellers with high or medium operational risk |
| `vw_high_risk_categories` | Product categories with high or medium operational risk |
| `vw_operational_event_summary` | Summary of event-driven operational event file processing |
| `vw_operational_event_records` | Detailed valid operational event records |
| `vw_operational_risk_summary` | Combined risk summary from anomaly alerts and operational event records |

These views will be used by Power BI, FastAPI endpoints, and the AI business insights assistant.


## dbt Transformation Layer

The project includes a dbt transformation layer to organise SQL transformations in a professional, modular, and testable structure.

dbt is used to manage the following transformation layers:

| dbt Folder | Purpose |
|---|---|
| `models/staging` | Cleans and standardises raw Olist tables |
| `models/warehouse` | Builds warehouse dimension and fact tables |
| `models/kpis` | Builds business KPI views |
| `models/operations` | Builds operational metric tables |
| `models/operational_kpis` | Builds operational KPI and risk views |

The dbt layer improves the project by adding a structured transformation workflow, clearer model organisation, and a foundation for dbt tests, documentation, and lineage.

The local dbt project is stored in:

`dbt_retail/`

The project uses SQLite for local development. In the cloud version, the same modelling approach will be migrated to Azure SQL Database.

## dbt Tests, Documentation, and Lineage

The project includes dbt schema files to document models and validate important data quality rules.

### dbt Test Coverage

dbt tests are used to validate:

| Test Type | Purpose |
|---|---|
| `not_null` | Ensures important fields are not missing |
| `unique` | Ensures primary keys and dimension keys are unique |
| `accepted_values` | Ensures status and risk fields contain valid values |
| `relationships` | Planned for validating relationships between fact and dimension tables |

### dbt Documentation

dbt documentation is generated using:

`dbt docs generate`

The generated documentation includes:

- Model descriptions
- Source descriptions
- Column descriptions
- Data tests
- Model lineage
- Source-to-model dependency graph

The documentation artifacts are created inside:

`dbt_retail/target/`

Important generated files include:

- `manifest.json`
- `catalog.json`
- `index.html`

The dbt lineage graph shows how raw Olist source tables flow into staging models, warehouse models, KPI views, operational metric models, and operational KPI views.

 ## Power BI Export Layer

The Power BI export layer creates CSV extracts from dbt-built warehouse tables, KPI views, operational metrics, and operational risk views.

The star schema tables are used as the main Power BI data model. KPI and operational views are used for executive summaries, anomaly reporting, and business-ready risk outputs.

### Core Power BI Model Tables

| Export | Description |
|---|---|
| `dim_date.csv` | Date dimension for time-based filtering and reporting |
| `dim_customer.csv` | Customer dimension for customer and geography analysis |
| `dim_product.csv` | Product dimension for product category analysis |
| `dim_seller.csv` | Seller dimension for seller performance analysis |
| `fact_sales.csv` | Main sales fact table |
| `fact_delivery.csv` | Delivery performance fact table |
| `fact_payments.csv` | Payment fact table |
| `fact_reviews.csv` | Review fact table |

### Business KPI Exports

| Export | Description |
|---|---|
| `vw_executive_summary.csv` | Executive-level KPI summary |
| `vw_monthly_sales.csv` | Monthly revenue and order trend |
| `vw_product_performance.csv` | Product category performance |
| `vw_seller_performance.csv` | Seller performance summary |
| `vw_customer_state_performance.csv` | Revenue and orders by customer state |
| `vw_delivery_performance.csv` | Delivery performance summary |
| `vw_payment_analysis.csv` | Payment method analysis |
| `vw_review_analysis.csv` | Review score analysis |
| `vw_late_delivery_by_state.csv` | Late delivery by customer state |
| `vw_category_review_performance.csv` | Category review performance |

### Operational and Anomaly Exports

| Export | Description |
|---|---|
| `ops_daily_metrics.csv` | Daily operational metrics |
| `ops_seller_metrics.csv` | Seller-level operational metrics |
| `ops_category_metrics.csv` | Category-level operational metrics |
| `vw_operational_alert_summary.csv` | Operational alert summary |
| `vw_operational_alerts_by_type.csv` | Alerts by anomaly type |
| `vw_operational_alerts_by_severity.csv` | Alerts by severity |
| `vw_recent_operational_alerts.csv` | Detailed alert records with recommended actions |
| `vw_high_risk_sellers.csv` | High-risk seller list |
| `vw_high_risk_categories.csv` | High-risk product category list |
| `vw_operational_risk_summary.csv` | Combined operational risk summary |
| `vw_operational_event_summary.csv` | Event pipeline processing summary |

The detailed event records are not exported for the main dashboard because the event pipeline is primarily a data engineering feature. The dashboard only uses the event summary as technical proof that the pipeline processed incoming files successfully.

 ## Full Pipeline Runner

The project includes a full local pipeline runner that executes the main data engineering workflow in the correct order.

The runner is stored in:

`scriptss/run_full_pipeline.py`

### Pipeline Steps

1. Raw file inspection
2. Raw data ingestion into SQLite
3. Raw database verification
4. Raw data quality checks
5. dbt transformations
6. dbt tests
7. Operational anomaly detection
8. Operational event file processing
9. Operational KPI view refresh
10. Power BI CSV export
11. Power BI export verification

### Main Command

```powershell
python scripts\run_full_pipeline.py
'''

## FastAPI Backend Layer

The FastAPI backend exposes curated project outputs through REST API endpoints.

The API serves:

- Executive KPI summaries
- Monthly sales trends
- Product and seller performance outputs
- Customer state performance
- Operational anomaly summaries
- Recent operational alerts
- High-risk sellers
- High-risk categories
- Operational risk summaries

The API reads from dbt-built tables and views in the SQLite database.

The local API documentation is available through Swagger UI at:

`http://127.0.0.1:8000/docs`


## Docker-Related Files

The project includes Docker-related files to support API containerisation and local deployment testing.

| File | Type | Purpose |
|---|---|---|
| `Dockerfile` | Docker build file | Defines how the FastAPI backend container image is built |
| `.dockerignore` | Docker configuration file | Excludes unnecessary files, generated files, and local database files from the Docker build context |
| `docker/README.md` | Documentation file | Provides detailed Docker build, run, volume mount, troubleshooting, and local-vs-cloud notes |
| `scripts/verify_docker_setup.py` | Python verification script | Validates Docker-related files and documentation |
| `data/processed/docker_setup_verification_report.csv` | Verification report | Stores the Docker setup verification results |

## Docker Image

| Item | Description |
|---|---|
| Image name | `ecommerce-retail-api` |
| Base image | `python:3.10-slim` |
| Main application | FastAPI backend |
| API server | Uvicorn |
| Exposed port | `8000` |
| Local database handling | SQLite database is mounted at runtime, not copied into the image |

## Docker Container

| Item | Description |
|---|---|
| Container name | `ecommerce-retail-api-container` |
| Local port | `8000` |
| Container port | `8000` |
| Runtime database mount | `retail_intelligence.db` mounted to `/app/retail_intelligence.db` |
| API documentation URL | `http://127.0.0.1:8000/docs` |
| Health endpoint | `http://127.0.0.1:8000/health/` |
| System status endpoint | `http://127.0.0.1:8000/health/status` |

## Docker Runtime Data Source

The local Docker container uses:

```text
retail_intelligence.db
```

This SQLite database contains the curated project tables and views used by the FastAPI backend.

The database file is mounted into the container at runtime using:

```powershell
-v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db
```

The local Docker version uses this file so the API can run as a self-contained demonstration without embedding a large generated database file inside the Docker image.

In the Azure version, the API will connect to Azure SQL Database instead.

## Docker-Served API Areas

The Docker container serves the same FastAPI routes as the local Python version.

| API Area | Purpose |
|---|---|
| Health endpoints | Validate API and database availability |
| Executive endpoints | Serve executive KPIs and sales summaries |
| Operations endpoints | Serve operational anomaly and risk outputs |
| Insights endpoints | Serve AI-ready business insights and LLM context |
| Authentication layer | Protect endpoints using API keys |
| RBAC layer | Restrict endpoint access by user role |

## Docker Verification Report

The Docker verification script creates:

```text
data/processed/docker_setup_verification_report.csv
```

This report checks whether expected Docker files and documentation sections exist.

Example checked items include:

- `Dockerfile`
- `.dockerignore`
- `docker/README.md`
- Docker build command documentation
- Docker run command documentation
- Docker volume mount documentation
- Docker architecture documentation
- Docker governance documentation

## Local vs Cloud Data Dictionary Note

| Area | Local Docker Version | Future Azure Version |
|---|---|---|
| API runtime | Docker container | Azure-hosted API |
| Database | SQLite database mounted at runtime | Azure SQL Database |
| Secrets | Demo API keys | Azure Key Vault |
| Monitoring | Local logs | Azure Monitor |
| Deployment | Manual Docker commands | CI/CD pipeline |


## CI/CD-Related Files

The project includes GitHub Actions CI files to support automated validation.

| File | Type | Purpose |
|---|---|---|
| `.github/workflows/ci.yml` | GitHub Actions workflow | Runs automated CI checks on GitHub |
| `scripts/verify_ci_setup.py` | Python verification script | Validates CI workflow and documentation setup |
| `data/processed/ci_setup_verification_report.csv` | Verification report | Stores CI setup verification results |

## CI Workflow

| Item | Description |
|---|---|
| Workflow name | `CI Pipeline` |
| Workflow file | `.github/workflows/ci.yml` |
| Trigger | Push, pull request, and manual workflow dispatch |
| Runner | `ubuntu-latest` |
| Python version | `3.10` |
| Dependency command | `pip install -r requirements.txt` |
| Syntax validation command | `python -m compileall src scripts` |
| Docker verification command | `python scripts/verify_docker_setup.py` |
| CI verification command | `python scripts/verify_ci_setup.py` |
| Docker build command | `docker build -t ecommerce-retail-api .` |

## CI Setup Verification Report

The CI setup verification report is generated by:

```text
scripts/verify_ci_setup.py
```

The report is saved to:

```text
data/processed/ci_setup_verification_report.csv
```

The CI setup verification report checks whether the expected CI workflow, documentation, Docker validation, and Git ignore rules are present.

Example checked items include:

- `.github/workflows/ci.yml`
- `scripts/verify_ci_setup.py`
- Main README CI documentation
- CI architecture documentation
- CI governance documentation
- Docker build validation command
- Database-independent CI notes

## CI Database Note

The local SQLite database file:

```text
retail_intelligence.db
```

is not committed to GitHub because it is a large generated artifact.

The CI workflow therefore uses database-independent checks.

Database-backed tests are currently run locally and can be added to CI later using Azure SQL Database or a smaller CI test database.

## CI Scope

The current CI workflow validates:

- Repository safety checks
- Python dependency installation
- Python syntax validation
- Core module import validation
- Docker setup verification
- CI setup verification
- Docker image build

Continuous Deployment is planned for a later phase after Azure deployment components are completed.