{{ config(materialized='view') }}

SELECT
    dc.customer_state,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    COUNT(*) AS total_order_items,
    ROUND(SUM(fs.item_price), 2) AS product_revenue,
    ROUND(SUM(fs.freight_value), 2) AS freight_revenue,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fs.item_total_value), 2) AS avg_item_total_value
FROM {{ ref('fact_sales') }} fs
LEFT JOIN {{ ref('dim_customer') }} dc
    ON fs.customer_key = dc.customer_key
GROUP BY
    dc.customer_state
ORDER BY
    total_revenue DESC