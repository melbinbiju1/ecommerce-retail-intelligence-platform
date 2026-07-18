
    
    create view main."vw_product_performance" as
    

SELECT
    dp.product_category_name_english,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(fs.item_price), 2) AS product_revenue,
    ROUND(SUM(fs.freight_value), 2) AS freight_revenue,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fs.item_price), 2) AS avg_item_price
FROM main."fact_sales" fs
LEFT JOIN main."dim_product" dp
    ON fs.product_key = dp.product_key
GROUP BY
    dp.product_category_name_english
ORDER BY
    total_revenue DESC;