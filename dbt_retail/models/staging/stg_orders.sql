{{ config(materialized='table') }}

SELECT
    order_id,
    customer_id,
    LOWER(TRIM(order_status)) AS order_status,
    datetime(order_purchase_timestamp) AS order_purchase_timestamp,
    datetime(order_approved_at) AS order_approved_at,
    datetime(order_delivered_carrier_date) AS order_delivered_carrier_date,
    datetime(order_delivered_customer_date) AS order_delivered_customer_date,
    datetime(order_estimated_delivery_date) AS order_estimated_delivery_date,

    CASE
        WHEN order_status = 'delivered' THEN 1
        ELSE 0
    END AS is_delivered,

    CASE
        WHEN order_status = 'delivered'
         AND order_delivered_customer_date IS NULL THEN 1
        ELSE 0
    END AS has_missing_delivery_date,

    CASE
        WHEN order_delivered_customer_date IS NOT NULL
         AND order_estimated_delivery_date IS NOT NULL
         AND datetime(order_delivered_customer_date) > datetime(order_estimated_delivery_date)
        THEN 1
        ELSE 0
    END AS is_late_delivery,

    CASE
        WHEN order_delivered_customer_date IS NOT NULL
         AND order_purchase_timestamp IS NOT NULL
        THEN CAST(
            julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)
            AS INTEGER
        )
        ELSE NULL
    END AS delivery_days,

    _source_file,
    _loaded_at
FROM {{ source('raw', 'raw_orders') }}