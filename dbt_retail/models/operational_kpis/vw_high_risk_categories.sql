{{ config(materialized='view') }}

SELECT
    product_category_name_english,
    total_orders,
    total_items_sold,
    total_revenue,
    avg_item_price,
    avg_review_score,
    late_delivery_items,
    late_delivery_rate,
    category_risk_level
FROM {{ ref('ops_category_metrics') }}
WHERE category_risk_level IN ('high', 'medium')
ORDER BY
    CASE category_risk_level
        WHEN 'high' THEN 1
        WHEN 'medium' THEN 2
        ELSE 3
    END,
    late_delivery_rate DESC,
    total_revenue DESC