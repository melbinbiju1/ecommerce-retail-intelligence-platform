

SELECT
    seller_id,
    seller_city,
    seller_state,
    total_orders,
    total_items_sold,
    total_revenue,
    avg_item_value,
    late_delivery_items,
    late_delivery_rate,
    avg_review_score,
    seller_risk_level
FROM main."ops_seller_metrics"
WHERE seller_risk_level IN ('high', 'medium')
ORDER BY
    CASE seller_risk_level
        WHEN 'high' THEN 1
        WHEN 'medium' THEN 2
        ELSE 3
    END,
    late_delivery_rate DESC,
    total_revenue DESC