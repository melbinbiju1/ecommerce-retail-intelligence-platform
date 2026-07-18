

SELECT
    ds.seller_id,
    ds.seller_city,
    ds.seller_state,

    COUNT(DISTINCT fs.order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fs.item_total_value), 2) AS avg_item_value,

    SUM(fs.is_late_delivery) AS late_delivery_items,
    ROUND(
        100.0 * SUM(fs.is_late_delivery) / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_rate,

    ROUND(AVG(fr.review_score), 2) AS avg_review_score,

    CASE
        WHEN ROUND(100.0 * SUM(fs.is_late_delivery) / NULLIF(COUNT(*), 0), 2) >= 30
             OR ROUND(AVG(fr.review_score), 2) <= 2.5
        THEN 'high'
        WHEN ROUND(100.0 * SUM(fs.is_late_delivery) / NULLIF(COUNT(*), 0), 2) >= 15
             OR ROUND(AVG(fr.review_score), 2) <= 3.5
        THEN 'medium'
        ELSE 'low'
    END AS seller_risk_level,

    datetime('now') AS created_at
FROM main."fact_sales" fs
LEFT JOIN main."dim_seller" ds
    ON fs.seller_key = ds.seller_key
LEFT JOIN main."fact_reviews" fr
    ON fs.order_id = fr.order_id
GROUP BY
    ds.seller_id,
    ds.seller_city,
    ds.seller_state