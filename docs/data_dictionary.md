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


## Azure SQL Database Files

The project includes Azure SQL files to support cloud database connectivity, migration, and verification.

| File | Type | Purpose |
|---|---|---|
| `src/cloud/azure_sql_database.py` | Python module | Loads Azure SQL configuration and creates SQLAlchemy connection engine |
| `scripts/test_azure_sql_connection.py` | Python script | Tests Azure SQL Database connectivity |
| `scripts/migrate_curated_data_to_azure_sql.py` | Python script | Migrates selected curated SQLite objects into Azure SQL |
| `scripts/verify_azure_sql_setup.py` | Python script | Verifies Azure SQL setup and loaded table row counts |
| `docs/azure_sql_database.md` | Documentation file | Documents Azure SQL architecture, migration, governance, and verification |
| `data/processed/azure_sql_connection_test_report.csv` | Report | Stores Azure SQL connection test result |
| `data/processed/azure_sql_migration_report.csv` | Report | Stores Azure SQL migration status and row counts |
| `data/processed/azure_sql_setup_verification_report.csv` | Report | Stores Azure SQL setup verification results |

## Azure SQL Environment Variables

| Variable | Purpose |
|---|---|
| `AZURE_SQL_SERVER` | Azure SQL server hostname |
| `AZURE_SQL_DATABASE` | Azure SQL database name |
| `AZURE_SQL_USERNAME` | SQL authentication username |
| `AZURE_SQL_PASSWORD` | SQL authentication password |
| `AZURE_SQL_DRIVER` | Local ODBC driver used by `pyodbc` |

Real values are stored only in the local `.env` file.

Safe placeholders are stored in `.env.example`.

## Azure SQL Loaded Tables

### Dimension Tables

| Table | Description | Rows Loaded |
|---|---|---:|
| `dim_date` | Date dimension for calendar-based analysis | 732 |
| `dim_customer` | Customer dimension with customer and location attributes | 99,441 |
| `dim_product` | Product dimension with product and category attributes | 32,951 |
| `dim_seller` | Seller dimension with seller location attributes | 3,095 |

### Fact Tables

| Table | Description | Rows Loaded |
|---|---|---:|
| `fact_sales` | Sales fact table with order item commercial metrics | 112,650 |
| `fact_delivery` | Delivery fact table with delivery performance metrics | 99,441 |
| `fact_payments` | Payment fact table with payment method and value data | 103,886 |
| `fact_reviews` | Review fact table with customer review metrics | 99,224 |

### Operational Tables

| Table | Description | Rows Loaded |
|---|---|---:|
| `ops_daily_metrics` | Daily operational KPI table | 616 |
| `ops_seller_metrics` | Seller-level operational metrics | 3,095 |
| `ops_category_metrics` | Category-level operational metrics | 74 |
| `ops_anomaly_rules` | Operational anomaly rule definitions | 8 |
| `ops_anomaly_alerts` | Operational anomaly alerts generated by rule-based detection | 696 |
| `ops_event_log` | Event pipeline processing log | 1 |
| `ops_event_records` | Processed event pipeline records | 100 |

## Azure SQL Migration Report

The migration report is written to:

```text
data/processed/azure_sql_migration_report.csv
```

The report includes:

- `object_name`
- `status`
- `row_count`
- `started_at`
- `finished_at`
- `error`

## Azure SQL Verification Report

The verification report is written to:

```text
data/processed/azure_sql_setup_verification_report.csv
```

The report validates:

- Local Azure SQL files
- `.env.example` placeholders
- Required Python dependencies
- Azure SQL table existence
- Azure SQL row counts


## Azure Data Factory Files and Objects

| Item | Type | Purpose |
|---|---|---|
| `docs/azure_data_factory.md` | Documentation | Documents ADF orchestration design |
| `sql/azure_sql/create_adf_staging_tables.sql` | SQL script | Creates ADF staging table in Azure SQL |
| `scripts/create_adf_staging_tables.py` | Python script | Executes ADF staging table SQL |
| `scripts/verify_adf_pipeline_output.py` | Python script | Verifies rows copied by ADF |
| `data/processed/adf_pipeline_output_verification_report.csv` | Report | Stores ADF output verification results |

## ADF Staging Table

| Table | Purpose |
|---|---|
| `dbo.adf_stg_orders_raw` | Stores raw order CSV data copied from Azure Blob Storage by ADF |

## ADF Pipeline Objects

| Object | Name |
|---|---|
| Data Factory | `adf-ecommerce-retail-intelligence` |
| Pipeline | `pl_copy_olist_orders_blob_to_sql` |
| Copy activity | `copy_olist_orders_to_sql` |
| Source dataset | `ds_blob_olist_orders_raw_csv` |
| Sink dataset | `ds_sql_adf_stg_orders_raw` |
| Source linked service | `ls_azure_blob_olist_raw` |
| Sink linked service | `ls_azure_sql_retail` |


## Azure App Deployment Outputs

This section documents the deployment-related files and outputs for the Azure App Service phase.

### Deployment Script Outputs

| File | Description |
|---|---|
| `scripts/verify_azure_app_deployment.py` | Verifies that the deployed Azure App Service API endpoints are responding successfully |
| `data/processed/azure_app_deployment_verification_report.csv` | CSV report showing endpoint checks, URLs, HTTP status codes, pass/fail status, and response previews |

### Azure App Service Runtime Variables

| Variable | Description |
|---|---|
| `APP_ENV` | Controls whether the API uses SQLite or Azure SQL Database |
| `AZURE_SQL_SERVER` | Azure SQL Server hostname |
| `AZURE_SQL_DATABASE` | Azure SQL Database name |
| `AZURE_SQL_USERNAME` | Azure SQL login username |
| `AZURE_SQL_PASSWORD` | Azure SQL login password |
| `AZURE_SQL_DRIVER` | ODBC driver used for Azure SQL connectivity |
| `ADMIN_API_KEY` | API key for admin-level access |
| `ANALYST_API_KEY` | API key for analyst-level access |
| `VIEWER_API_KEY` | API key for viewer-level access |
| `WEBSITES_PORT` | Container port used by Azure App Service |
| `AZURE_APP_BASE_URL` | Base URL used by local verification scripts to test the deployed API |

### Azure App Verification Report Columns

File:

```text
data/processed/azure_app_deployment_verification_report.csv
```

| Column | Description |
|---|---|
| `check_name` | Name of the endpoint check |
| `url` | Full deployed API URL tested |
| `status_code` | HTTP status code returned by the endpoint |
| `passed` | Boolean flag showing whether the check passed |
| `response_preview` | Short preview of the API response body |

### API Serving Objects Required in Azure SQL

The deployed API requires the following serving-layer objects in Azure SQL:

| Object | Purpose |
|---|---|
| `vw_executive_summary` | Executive KPI summary |
| `vw_monthly_sales` | Monthly sales performance |
| `vw_product_performance` | Product category performance |
| `vw_seller_performance` | Seller performance |
| `vw_customer_state_performance` | Customer state performance |
| `vw_operational_alert_summary` | Operational alert summary |
| `vw_operational_alerts_by_type` | Alerts grouped by anomaly type |
| `vw_operational_alerts_by_severity` | Alerts grouped by severity |
| `vw_recent_operational_alerts` | Recent anomaly alert records |
| `vw_high_risk_sellers` | Sellers with elevated operational risk |
| `vw_high_risk_categories` | Product categories with elevated operational risk |
| `vw_operational_risk_summary` | Overall operational risk summary |

These objects are migrated to Azure SQL using:

```powershell
python scripts\migrate_api_serving_views_to_azure_sql.py
```

## Azure Key Vault Verification Outputs

This section documents files and configuration related to Azure Key Vault secret management.

### Verification Script

| File | Description |
|---|---|
| `scripts/verify_key_vault_setup.py` | Verifies that the deployed API still works after App Service settings are changed to Key Vault references |

### Verification Report

| File | Description |
|---|---|
| `data/processed/key_vault_setup_verification_report.csv` | CSV report containing endpoint checks after Key Vault integration |

### Verification Report Columns

| Column | Description |
|---|---|
| `check_name` | Name of the verification check |
| `url` | Deployed API endpoint tested |
| `status_code` | HTTP status code returned by the endpoint |
| `passed` | Boolean result showing whether the check passed |
| `response_preview` | Short preview of the API response body |

### Key Vault Secret Names

| Secret name | Used by App Setting |
|---|---|
| `azure-sql-server` | `AZURE_SQL_SERVER` |
| `azure-sql-database` | `AZURE_SQL_DATABASE` |
| `azure-sql-username` | `AZURE_SQL_USERNAME` |
| `azure-sql-password` | `AZURE_SQL_PASSWORD` |
| `admin-api-key` | `ADMIN_API_KEY` |
| `analyst-api-key` | `ANALYST_API_KEY` |
| `viewer-api-key` | `VIEWER_API_KEY` |

### App Service Key Vault Reference Format

```text
@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=<secret-name>)
```

### Non-Secret Runtime Settings

| Setting | Purpose |
|---|---|
| `APP_ENV` | Tells the API to run in local or Azure mode |
| `AZURE_SQL_DRIVER` | Defines the ODBC driver used for Azure SQL |
| `WEBSITES_PORT` | Tells App Service which port the container listens on |
| `AZURE_APP_BASE_URL` | Used locally by verification scripts to test the deployed API |
| `AZURE_KEY_VAULT_NAME` | Documents the configured Azure Key Vault name |


## Azure Monitoring Verification Outputs

This section documents files and outputs related to Azure monitoring setup.

### Monitoring Verification Script

| File | Description |
|---|---|
| `scripts/verify_azure_monitoring_setup.py` | Verifies monitoring setup evidence and deployed API endpoint availability |

### Monitoring Verification Report

| File | Description |
|---|---|
| `data/processed/azure_monitoring_setup_verification_report.csv` | CSV report containing manual monitoring setup checks and automated deployed endpoint checks |

### Report Columns

| Column | Description |
|---|---|
| `check_name` | Name of the monitoring verification check |
| `component` | Azure service or API component being checked |
| `expected_configuration` | Expected setup or endpoint behavior |
| `verification_method` | Manual or automated verification method |
| `url` | Endpoint URL tested, if applicable |
| `status_code` | HTTP status code returned by endpoint checks |
| `passed` | Boolean pass/fail result |
| `response_preview` | Short preview of the endpoint response |
| `checked_at_utc` | UTC timestamp when the check was recorded |

### Monitoring Resources

| Resource | Purpose |
|---|---|
| `appi-ecommerce-retail-api` | Application Insights resource for the deployed API |
| `fastapi-health-check` | Availability test for the deployed `/health/` endpoint |
| Automatic availability alert rule | Alerts when multiple availability test locations fail |
| App Service Log Stream | Provides live application/container log visibility |

### Monitored Endpoints

| Endpoint | Purpose |
|---|---|
| `/health/` | Public API and database health check |
| `/executive/summary` | Protected executive KPI endpoint used in verification |
| `/operations/alert-summary` | Protected operations monitoring endpoint used in verification |


## Final Technical Documentation Artifacts

This section documents the final technical documentation files created after the Azure deployment, Key Vault, and monitoring phases.

These files explain the complete implemented architecture of the platform.

### Final Architecture Documentation Files

| File | Description |
|---|---|
| `docs/final_architecture.md` | Clean final end-to-end architecture summary of the implemented platform |
| `docs/technical_architecture.md` | Detailed technical design decisions, runtime modes, trade-offs, security, deployment, monitoring, and verification architecture |
| `docs/system_flow.md` | Step-by-step explanation of data flow, API request flow, deployment flow, secret flow, monitoring flow, and verification flow |
| `docs/architecture.md` | Detailed working architecture document updated throughout the project |

---

## Final Platform Layers

| Layer | Main Artifacts |
|---|---|
| Source data layer | Olist CSV files |
| Local ingestion layer | Python ingestion scripts, SQLite raw tables |
| Data quality layer | Data quality scripts and validation reports |
| Staging layer | SQL staging tables, dbt staging models |
| Warehouse layer | Dimension tables, fact tables, KPI views |
| Operational intelligence layer | Operational metrics, anomaly rules, anomaly alerts, event records |
| Power BI export layer | Dashboard-ready export files |
| Azure Blob Storage layer | Raw files in `raw/olist/` |
| Azure Data Factory layer | Pipeline, linked services, datasets, SQL staging table |
| Azure SQL layer | Curated cloud tables and API serving objects |
| FastAPI layer | API routes, authentication, RBAC, insight endpoints |
| Docker layer | Dockerfile, `.dockerignore`, Docker image |
| Azure Container Registry layer | Pushed API container image |
| Azure App Service layer | Deployed FastAPI container |
| Azure Key Vault layer | SQL credentials and API key secrets |
| Azure Monitoring layer | App Service logs, Application Insights availability test, alert rule |

---

## Final Verification Reports

The project produces verification reports that provide evidence for major platform layers.

| Report File | Purpose |
|---|---|
| `data/processed/automated_test_run_summary.csv` | Summarizes automated test execution |
| `data/processed/azure_blob_upload_report.csv` | Documents raw file upload results to Azure Blob Storage |
| `data/processed/azure_sql_connection_test_report.csv` | Records Azure SQL connection test result |
| `data/processed/azure_sql_setup_verification_report.csv` | Verifies Azure SQL table availability and row counts |
| `data/processed/adf_pipeline_output_verification_report.csv` | Verifies ADF pipeline output in Azure SQL |
| `data/processed/azure_app_deployment_verification_report.csv` | Verifies deployed Azure App Service API endpoints |
| `data/processed/key_vault_setup_verification_report.csv` | Verifies deployed API works after Key Vault integration |
| `data/processed/azure_monitoring_setup_verification_report.csv` | Verifies monitoring evidence and deployed endpoint availability |

---

## Final Technical Scripts Index

This section summarizes important scripts used across the final technical build.

| Script | Purpose |
|---|---|
| `scripts/run_tests.py` | Runs automated unit, API, RBAC, and integration tests |
| `scripts/upload_raw_data_to_blob.py` | Uploads raw CSV files to Azure Blob Storage |
| `scripts/verify_azure_blob_setup.py` | Verifies Azure Blob Storage setup |
| `scripts/test_azure_sql_connection.py` | Tests Azure SQL Database connectivity |
| `scripts/migrate_curated_data_to_azure_sql.py` | Migrates curated SQLite tables into Azure SQL |
| `scripts/migrate_api_serving_views_to_azure_sql.py` | Migrates API serving objects to Azure SQL |
| `scripts/verify_azure_sql_setup.py` | Verifies Azure SQL tables and row counts |
| `scripts/create_adf_staging_tables.py` | Creates Azure SQL staging tables used by ADF |
| `scripts/verify_adf_setup.py` | Verifies ADF-related files and documentation |
| `scripts/verify_adf_pipeline_output.py` | Verifies copied ADF staging data in Azure SQL |
| `scripts/verify_azure_app_deployment.py` | Verifies deployed Azure App Service API endpoints |
| `scripts/verify_key_vault_setup.py` | Verifies Key Vault-based deployment still works |
| `scripts/verify_azure_monitoring_setup.py` | Verifies monitoring setup evidence and endpoint availability |

---

## Final API Serving Objects

The deployed API reads curated serving objects from Azure SQL when running in cloud mode.

| Serving Object | Used By |
|---|---|
| `vw_executive_summary` | `/executive/summary` |
| `vw_monthly_sales` | `/executive/monthly-sales` |
| `vw_product_performance` | `/executive/top-products` |
| `vw_seller_performance` | `/executive/top-sellers` |
| `vw_customer_state_performance` | `/executive/customer-states` |
| `vw_operational_alert_summary` | `/operations/alert-summary` |
| `vw_operational_alerts_by_type` | `/operations/alerts-by-type` |
| `vw_operational_alerts_by_severity` | `/operations/alerts-by-severity` |
| `vw_recent_operational_alerts` | `/operations/recent-alerts` |
| `vw_high_risk_sellers` | `/operations/high-risk-sellers` |
| `vw_high_risk_categories` | `/operations/high-risk-categories` |
| `vw_operational_risk_summary` | `/operations/risk-summary` |

---

## Final Environment Configuration Groups

The project uses environment variables to separate configuration from source code.

| Group | Examples |
|---|---|
| API runtime | `APP_ENV`, `WEBSITES_PORT` |
| API security | `ADMIN_API_KEY`, `ANALYST_API_KEY`, `VIEWER_API_KEY` |
| Azure Blob Storage | `AZURE_STORAGE_CONNECTION_STRING`, `AZURE_BLOB_CONTAINER_NAME`, `AZURE_BLOB_RAW_PREFIX` |
| Azure SQL Database | `AZURE_SQL_SERVER`, `AZURE_SQL_DATABASE`, `AZURE_SQL_USERNAME`, `AZURE_SQL_PASSWORD`, `AZURE_SQL_DRIVER` |
| Azure App Service | `AZURE_APP_BASE_URL` |
| Azure Key Vault | `AZURE_KEY_VAULT_NAME` |
| Azure Monitoring | `AZURE_APPLICATION_INSIGHTS_NAME`, `AZURE_MONITOR_AVAILABILITY_TEST_NAME` |

The real `.env` file is local-only and must not be committed to Git.

Safe placeholder values are documented in `.env.example`.

---

## Final Technical Completion Evidence

The project is technically complete when the following are true:

```text
Automated tests pass
Docker verification passes
GitHub Actions CI passes
Azure Blob Storage verification passes
Azure SQL verification passes
ADF setup and output verification pass
Azure App deployment verification passes
Azure Key Vault verification passes
Azure Monitoring verification passes
Final architecture documentation exists
```

This evidence supports the final technical architecture before portfolio packaging and dashboard presentation.