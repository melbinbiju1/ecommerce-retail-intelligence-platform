
  
    
    
    create  table main."ops_category_metrics"
    as
        

SELECT
    dp.product_category_name_english,

    COUNT(DISTINCT fs.order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fs.item_price), 2) AS avg_item_price,

    ROUND(AVG(fr.review_score), 2) AS avg_review_score,

    SUM(fs.is_late_delivery) AS late_delivery_items,
    ROUND(
        100.0 * SUM(fs.is_late_delivery) / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_rate,

    CASE
        WHEN ROUND(100.0 * SUM(fs.is_late_delivery) / NULLIF(COUNT(*), 0), 2) >= 30
             OR ROUND(AVG(fr.review_score), 2) <= 2.5
        THEN 'high'
        WHEN ROUND(100.0 * SUM(fs.is_late_delivery) / NULLIF(COUNT(*), 0), 2) >= 15
             OR ROUND(AVG(fr.review_score), 2) <= 3.5
        THEN 'medium'
        ELSE 'low'
    END AS category_risk_level,

    datetime('now') AS created_at
FROM main."fact_sales" fs
LEFT JOIN main."dim_product" dp
    ON fs.product_key = dp.product_key
LEFT JOIN main."fact_reviews" fr
    ON fs.order_id = fr.order_id
GROUP BY
    dp.product_category_name_english

  