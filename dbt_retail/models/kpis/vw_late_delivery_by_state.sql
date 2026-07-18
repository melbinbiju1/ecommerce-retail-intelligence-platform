{{ config(materialized='view') }}

SELECT
    dc.customer_state,
    COUNT(DISTINCT fd.order_id) AS total_orders,
    SUM(fd.is_late_delivery) AS late_orders,
    ROUND(
        100.0 * SUM(fd.is_late_delivery) / COUNT(DISTINCT fd.order_id),
        2
    ) AS late_order_percentage,
    ROUND(AVG(fd.delivery_days), 2) AS avg_delivery_days
FROM {{ ref('fact_delivery') }} fd
LEFT JOIN {{ ref('dim_customer') }} dc
    ON fd.customer_key = dc.customer_key
GROUP BY
    dc.customer_state
ORDER BY
    late_order_percentage DESC