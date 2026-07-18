{{ config(materialized='view') }}

SELECT
    fd.order_status,
    COUNT(DISTINCT fd.order_id) AS total_orders,
    SUM(fd.is_delivered) AS delivered_orders,
    SUM(fd.is_late_delivery) AS late_deliveries,
    SUM(fd.has_missing_delivery_date) AS missing_delivery_date_orders,
    ROUND(AVG(fd.delivery_days), 2) AS avg_delivery_days,
    MIN(fd.delivery_days) AS min_delivery_days,
    MAX(fd.delivery_days) AS max_delivery_days
FROM {{ ref('fact_delivery') }} fd
GROUP BY
    fd.order_status
ORDER BY
    total_orders DESC