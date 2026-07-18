
  
    
    
    create  table main."dim_date"
    as
        

WITH all_dates AS (
    SELECT date(order_purchase_timestamp) AS date_value FROM main."stg_orders" WHERE order_purchase_timestamp IS NOT NULL
    UNION
    SELECT date(order_approved_at) AS date_value FROM main."stg_orders" WHERE order_approved_at IS NOT NULL
    UNION
    SELECT date(order_delivered_carrier_date) AS date_value FROM main."stg_orders" WHERE order_delivered_carrier_date IS NOT NULL
    UNION
    SELECT date(order_delivered_customer_date) AS date_value FROM main."stg_orders" WHERE order_delivered_customer_date IS NOT NULL
    UNION
    SELECT date(order_estimated_delivery_date) AS date_value FROM main."stg_orders" WHERE order_estimated_delivery_date IS NOT NULL
    UNION
    SELECT date(shipping_limit_date) AS date_value FROM main."stg_order_items" WHERE shipping_limit_date IS NOT NULL
    UNION
    SELECT date(review_creation_date) AS date_value FROM main."stg_order_reviews" WHERE review_creation_date IS NOT NULL
)
SELECT
    CAST(strftime('%Y%m%d', date_value) AS INTEGER) AS date_key,
    date_value AS full_date,
    CAST(strftime('%d', date_value) AS INTEGER) AS day,
    CAST(strftime('%m', date_value) AS INTEGER) AS month,
    CAST(strftime('%Y', date_value) AS INTEGER) AS year,
    CAST(strftime('%W', date_value) AS INTEGER) AS week_of_year,
    CASE
        WHEN CAST(strftime('%m', date_value) AS INTEGER) BETWEEN 1 AND 3 THEN 1
        WHEN CAST(strftime('%m', date_value) AS INTEGER) BETWEEN 4 AND 6 THEN 2
        WHEN CAST(strftime('%m', date_value) AS INTEGER) BETWEEN 7 AND 9 THEN 3
        ELSE 4
    END AS quarter,
    strftime('%Y-%m', date_value) AS year_month
FROM all_dates
WHERE date_value IS NOT NULL

  