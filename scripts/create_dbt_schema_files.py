from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DBT_MODELS_DIR = PROJECT_ROOT / "dbt_retail" / "models"


STAGING_SCHEMA = """
version: 2

sources:
  - name: raw
    database: retail_intelligence
    schema: main
    description: "Raw Olist source tables loaded from CSV files using Python ingestion."
    tables:
      - name: raw_customers
        description: "Raw customer records from the Olist customers dataset."
      - name: raw_geolocation
        description: "Raw Brazilian zip-code geolocation reference data."
      - name: raw_order_items
        description: "Raw order item records containing product, seller, price, and freight data."
      - name: raw_order_payments
        description: "Raw payment records containing payment type, installments, and value."
      - name: raw_order_reviews
        description: "Raw customer review records."
      - name: raw_orders
        description: "Raw order lifecycle records including purchase, approval, delivery, and estimated delivery dates."
      - name: raw_products
        description: "Raw product records and product attributes."
      - name: raw_sellers
        description: "Raw seller records and seller location details."
      - name: raw_product_category_translation
        description: "Product category translation from Portuguese to English."

models:
  - name: stg_customers
    description: "Cleaned customer dimension staging model."
    columns:
      - name: customer_id
        description: "Unique customer identifier used in orders."
        tests:
          - not_null
          - unique
      - name: customer_unique_id
        description: "Unique customer person identifier."
        tests:
          - not_null
      - name: customer_state
        description: "Customer state code."
        tests:
          - not_null

  - name: stg_sellers
    description: "Cleaned seller staging model."
    columns:
      - name: seller_id
        description: "Unique seller identifier."
        tests:
          - not_null
          - unique
      - name: seller_state
        description: "Seller state code."
        tests:
          - not_null

  - name: stg_product_category_translation
    description: "Product category translation staging model."
    columns:
      - name: product_category_name
        tests:
          - not_null
          - unique
      - name: product_category_name_english
        tests:
          - not_null

  - name: stg_products
    description: "Cleaned product staging model with English category names."
    columns:
      - name: product_id
        description: "Unique product identifier."
        tests:
          - not_null
          - unique

  - name: stg_orders
    description: "Cleaned order lifecycle staging model with delivery flags."
    columns:
      - name: order_id
        description: "Unique order identifier."
        tests:
          - not_null
          - unique
      - name: customer_id
        description: "Customer identifier."
        tests:
          - not_null
      - name: order_status
        description: "Order lifecycle status."
        tests:
          - not_null
          - accepted_values:
              values: ['delivered', 'shipped', 'canceled', 'unavailable', 'invoiced', 'processing', 'created', 'approved']

  - name: stg_order_items
    description: "Cleaned order item staging model."
    columns:
      - name: order_id
        tests:
          - not_null
      - name: product_id
        tests:
          - not_null
      - name: seller_id
        tests:
          - not_null

  - name: stg_order_payments
    description: "Cleaned order payment staging model."
    columns:
      - name: order_id
        tests:
          - not_null
      - name: payment_type
        tests:
          - not_null

  - name: stg_order_reviews
    description: "Cleaned order review staging model."
    columns:
      - name: review_id
        tests:
          - not_null
      - name: order_id
        tests:
          - not_null
      - name: review_score
        tests:
          - not_null
          - accepted_values:
              values: [1, 2, 3, 4, 5]

  - name: stg_geolocation
    description: "Deduplicated geolocation staging model."
    columns:
      - name: geolocation_zip_code_prefix
        tests:
          - not_null
"""


WAREHOUSE_SCHEMA = """
version: 2

models:
  - name: dim_date
    description: "Date dimension used for time-based analysis."
    columns:
      - name: date_key
        description: "Surrogate date key."
        tests:
          - not_null
          - unique
      - name: full_date
        description: "Calendar date."

  - name: dim_customer
    description: "Customer dimension with location attributes."
    columns:
      - name: customer_key
        description: "Customer surrogate key."
        tests:
          - not_null
          - unique
      - name: customer_id
        tests:
          - not_null
          - unique

  - name: dim_seller
    description: "Seller dimension with seller location attributes."
    columns:
      - name: seller_key
        description: "Seller surrogate key."
        tests:
          - not_null
          - unique
      - name: seller_id
        tests:
          - not_null
          - unique

  - name: dim_product
    description: "Product dimension with category and product attributes."
    columns:
      - name: product_key
        description: "Product surrogate key."
        tests:
          - not_null
          - unique
      - name: product_id
        tests:
          - not_null
          - unique

  - name: fact_sales
    description: "Main order-item level sales fact table."
    columns:
      - name: order_id
        tests:
          - not_null
      - name: customer_key
        tests:
          - not_null
      - name: product_key
        tests:
          - not_null
      - name: seller_key
        tests:
          - not_null
      - name: item_total_value
        description: "Item price plus freight value."

  - name: fact_delivery
    description: "Order-level delivery performance fact table."
    columns:
      - name: order_id
        tests:
          - not_null
          - unique
      - name: order_status
        tests:
          - not_null

  - name: fact_payments
    description: "Payment transaction fact table."
    columns:
      - name: order_id
        tests:
          - not_null
      - name: payment_type
        tests:
          - not_null

  - name: fact_reviews
    description: "Customer review fact table."
    columns:
      - name: review_id
        tests:
          - not_null
      - name: order_id
        tests:
          - not_null
      - name: review_score
        tests:
          - not_null
          - accepted_values:
              values: [1, 2, 3, 4, 5]
"""


KPIS_SCHEMA = """
version: 2

models:
  - name: vw_executive_summary
    description: "Executive-level summary of revenue, orders, customers, sellers, and delivery performance."
  - name: vw_monthly_sales
    description: "Monthly revenue and order trend."
  - name: vw_product_performance
    description: "Product category performance summary."
  - name: vw_seller_performance
    description: "Seller revenue and delivery performance summary."
  - name: vw_customer_state_performance
    description: "Revenue and order performance by customer state."
  - name: vw_delivery_performance
    description: "Delivery status and delivery duration summary."
  - name: vw_payment_analysis
    description: "Payment method and payment value summary."
  - name: vw_review_analysis
    description: "Review score distribution and customer satisfaction summary."
  - name: vw_late_delivery_by_state
    description: "Late delivery performance by customer state."
  - name: vw_category_review_performance
    description: "Product category review score and revenue summary."
"""


OPERATIONS_SCHEMA = """
version: 2

models:
  - name: ops_daily_metrics
    description: "Daily operational metrics used for anomaly detection and business monitoring."
    columns:
      - name: metric_date
        tests:
          - not_null
          - unique
      - name: total_orders
        tests:
          - not_null
      - name: total_revenue
        tests:
          - not_null

  - name: ops_seller_metrics
    description: "Seller-level operational metrics used to identify seller risk."
    columns:
      - name: seller_id
        tests:
          - not_null
          - unique
      - name: seller_risk_level
        tests:
          - not_null
          - accepted_values:
              values: ['low', 'medium', 'high']

  - name: ops_category_metrics
    description: "Product category-level operational metrics used to identify category risk."
    columns:
      - name: product_category_name_english
        tests:
          - not_null
          - unique
      - name: category_risk_level
        tests:
          - not_null
          - accepted_values:
              values: ['low', 'medium', 'high']
"""


OPERATIONAL_KPIS_SCHEMA = """
version: 2

sources:
  - name: operations_external
    database: retail_intelligence
    schema: main
    description: "Operational tables created by Python anomaly detection and event pipeline scripts."
    tables:
      - name: ops_anomaly_alerts
        description: "Operational anomaly alerts created by the Python anomaly detection script."
      - name: ops_anomaly_rules
        description: "Operational anomaly detection rule definitions."
      - name: ops_event_log
        description: "File-level operational event pipeline log."
      - name: ops_event_records
        description: "Valid operational event records processed by the event pipeline."
      - name: ops_event_failed_records
        description: "Invalid operational event records with failure reasons."

models:
  - name: vw_operational_alert_summary
    description: "Summary count of operational anomaly alerts by severity."
  - name: vw_operational_alerts_by_type
    description: "Operational anomaly alert counts by alert type and business area."
  - name: vw_operational_alerts_by_severity
    description: "Operational anomaly alert distribution by severity."
  - name: vw_recent_operational_alerts
    description: "Detailed operational alerts with descriptions and recommended actions."
  - name: vw_high_risk_sellers
    description: "Sellers with high or medium operational risk."
  - name: vw_high_risk_categories
    description: "Product categories with high or medium operational risk."
  - name: vw_operational_event_summary
    description: "Summary of operational event file processing."
  - name: vw_operational_event_records
    description: "Valid operational event records for monitoring."
  - name: vw_operational_risk_summary
    description: "Combined risk summary from anomaly alerts and event records."
"""


def write_file(relative_path: str, content: str) -> None:
    file_path = DBT_MODELS_DIR / relative_path
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {file_path.relative_to(PROJECT_ROOT)}")


def main() -> None:
    print("Creating dbt schema.yml files...")

    write_file("staging/schema.yml", STAGING_SCHEMA)
    write_file("warehouse/schema.yml", WAREHOUSE_SCHEMA)
    write_file("kpis/schema.yml", KPIS_SCHEMA)
    write_file("operations/schema.yml", OPERATIONS_SCHEMA)
    write_file("operational_kpis/schema.yml", OPERATIONAL_KPIS_SCHEMA)

    print("\ndbt schema files created successfully.")


if __name__ == "__main__":
    main()