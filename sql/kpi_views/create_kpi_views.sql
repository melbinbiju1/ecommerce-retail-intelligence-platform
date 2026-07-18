DROP VIEW IF EXISTS vw_executive_summary;
CREATE VIEW vw_executive_summary AS
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
FROM fact_sales fs;


DROP VIEW IF EXISTS vw_monthly_sales;
CREATE VIEW vw_monthly_sales AS
SELECT
    dd.year,
    dd.month,
    dd.year_month,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    COUNT(*) AS total_order_items,
    ROUND(SUM(fs.item_price), 2) AS product_revenue,
    ROUND(SUM(fs.freight_value), 2) AS freight_revenue,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fs.item_total_value), 2) AS avg_item_total_value
FROM fact_sales fs
LEFT JOIN dim_date dd
    ON fs.purchase_date_key = dd.date_key
GROUP BY
    dd.year,
    dd.month,
    dd.year_month
ORDER BY
    dd.year,
    dd.month;


DROP VIEW IF EXISTS vw_product_performance;
CREATE VIEW vw_product_performance AS
SELECT
    dp.product_category_name_english,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(fs.item_price), 2) AS product_revenue,
    ROUND(SUM(fs.freight_value), 2) AS freight_revenue,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fs.item_price), 2) AS avg_item_price
FROM fact_sales fs
LEFT JOIN dim_product dp
    ON fs.product_key = dp.product_key
GROUP BY
    dp.product_category_name_english
ORDER BY
    total_revenue DESC;


DROP VIEW IF EXISTS vw_seller_performance;
CREATE VIEW vw_seller_performance AS
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
FROM fact_sales fs
LEFT JOIN dim_seller ds
    ON fs.seller_key = ds.seller_key
GROUP BY
    ds.seller_id,
    ds.seller_city,
    ds.seller_state
ORDER BY
    total_revenue DESC;


DROP VIEW IF EXISTS vw_customer_state_performance;
CREATE VIEW vw_customer_state_performance AS
SELECT
    dc.customer_state,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    COUNT(*) AS total_order_items,
    ROUND(SUM(fs.item_price), 2) AS product_revenue,
    ROUND(SUM(fs.freight_value), 2) AS freight_revenue,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fs.item_total_value), 2) AS avg_item_total_value
FROM fact_sales fs
LEFT JOIN dim_customer dc
    ON fs.customer_key = dc.customer_key
GROUP BY
    dc.customer_state
ORDER BY
    total_revenue DESC;


DROP VIEW IF EXISTS vw_delivery_performance;
CREATE VIEW vw_delivery_performance AS
SELECT
    fd.order_status,
    COUNT(DISTINCT fd.order_id) AS total_orders,
    SUM(fd.is_delivered) AS delivered_orders,
    SUM(fd.is_late_delivery) AS late_deliveries,
    SUM(fd.has_missing_delivery_date) AS missing_delivery_date_orders,
    ROUND(AVG(fd.delivery_days), 2) AS avg_delivery_days,
    MIN(fd.delivery_days) AS min_delivery_days,
    MAX(fd.delivery_days) AS max_delivery_days
FROM fact_delivery fd
GROUP BY
    fd.order_status
ORDER BY
    total_orders DESC;


DROP VIEW IF EXISTS vw_payment_analysis;
CREATE VIEW vw_payment_analysis AS
SELECT
    payment_type,
    COUNT(*) AS payment_records,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_value), 2) AS avg_payment_value,
    ROUND(AVG(payment_installments), 2) AS avg_installments
FROM fact_payments
GROUP BY
    payment_type
ORDER BY
    total_payment_value DESC;


DROP VIEW IF EXISTS vw_review_analysis;
CREATE VIEW vw_review_analysis AS
SELECT
    fr.review_score,
    COUNT(*) AS review_count,
    SUM(fr.has_review_comment) AS reviews_with_comment,
    ROUND(AVG(fd.delivery_days), 2) AS avg_delivery_days,
    SUM(fd.is_late_delivery) AS late_delivery_orders
FROM fact_reviews fr
LEFT JOIN fact_delivery fd
    ON fr.order_id = fd.order_id
GROUP BY
    fr.review_score
ORDER BY
    fr.review_score;


DROP VIEW IF EXISTS vw_late_delivery_by_state;
CREATE VIEW vw_late_delivery_by_state AS
SELECT
    dc.customer_state,
    COUNT(DISTINCT fd.order_id) AS total_orders,
    SUM(fd.is_late_delivery) AS late_orders,
    ROUND(
        100.0 * SUM(fd.is_late_delivery) / COUNT(DISTINCT fd.order_id),
        2
    ) AS late_order_percentage,
    ROUND(AVG(fd.delivery_days), 2) AS avg_delivery_days
FROM fact_delivery fd
LEFT JOIN dim_customer dc
    ON fd.customer_key = dc.customer_key
GROUP BY
    dc.customer_state
ORDER BY
    late_order_percentage DESC;


DROP VIEW IF EXISTS vw_category_review_performance;
CREATE VIEW vw_category_review_performance AS
SELECT
    dp.product_category_name_english,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
    ROUND(AVG(fr.review_score), 2) AS avg_review_score,
    COUNT(fr.review_id) AS total_reviews
FROM fact_sales fs
LEFT JOIN dim_product dp
    ON fs.product_key = dp.product_key
LEFT JOIN fact_reviews fr
    ON fs.order_id = fr.order_id
GROUP BY
    dp.product_category_name_english
ORDER BY
    total_revenue DESC;