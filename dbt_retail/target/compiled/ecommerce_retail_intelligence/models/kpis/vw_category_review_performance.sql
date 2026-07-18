

SELECT
    dp.product_category_name_english,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fr.review_score), 2) AS avg_review_score,
    COUNT(fr.review_id) AS total_reviews
FROM main."fact_sales" fs
LEFT JOIN main."dim_product" dp
    ON fs.product_key = dp.product_key
LEFT JOIN main."fact_reviews" fr
    ON fs.order_id = fr.order_id
GROUP BY
    dp.product_category_name_english
ORDER BY
    total_revenue DESC