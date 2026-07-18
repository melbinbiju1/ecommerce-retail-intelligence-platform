
    
    create view main."vw_seller_performance" as
    

SELECT
    ds.seller_id,
    ds.seller_city,
    ds.seller_state,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(fs.item_price), 2) AS product_revenue,
    ROUND(SUM(fs.freight_value), 2) AS freight_revenue,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fs.item_total_value), 2) AS avg_item_total_value,
    SUM(fs.is_late_delivery) AS late_delivery_item_rows
FROM main."fact_sales" fs
LEFT JOIN main."dim_seller" ds
    ON fs.seller_key = ds.seller_key
GROUP BY
    ds.seller_id,
    ds.seller_city,
    ds.seller_state
ORDER BY
    total_revenue DESC;