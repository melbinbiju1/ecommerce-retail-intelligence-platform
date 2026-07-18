
    
    create view main."vw_executive_summary" as
    

SELECT
    COUNT(DISTINCT fs.order_id) AS total_orders,
    COUNT(*) AS total_order_items,
    ROUND(SUM(fs.item_price), 2) AS total_product_revenue,
    ROUND(SUM(fs.freight_value), 2) AS total_freight_revenue,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fs.item_price), 2) AS avg_item_price,
    ROUND(AVG(fs.freight_value), 2) AS avg_freight_value,
    ROUND(AVG(fs.item_total_value), 2) AS avg_item_total_value,
    SUM(fs.is_delivered) AS delivered_item_rows,
    SUM(fs.is_late_delivery) AS late_delivery_item_rows
FROM main."fact_sales" fs;