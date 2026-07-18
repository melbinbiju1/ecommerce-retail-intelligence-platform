DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date AS
WITH all_dates AS (
    SELECT date(order_purchase_timestamp) AS date_value FROM stg_orders WHERE order_purchase_timestamp IS NOT NULL
    UNION
    SELECT date(order_approved_at) AS date_value FROM stg_orders WHERE order_approved_at IS NOT NULL
    UNION
    SELECT date(order_delivered_carrier_date) AS date_value FROM stg_orders WHERE order_delivered_carrier_date IS NOT NULL
    UNION
    SELECT date(order_delivered_customer_date) AS date_value FROM stg_orders WHERE order_delivered_customer_date IS NOT NULL
    UNION
    SELECT date(order_estimated_delivery_date) AS date_value FROM stg_orders WHERE order_estimated_delivery_date IS NOT NULL
    UNION
    SELECT date(shipping_limit_date) AS date_value FROM stg_order_items WHERE shipping_limit_date IS NOT NULL
    UNION
    SELECT date(review_creation_date) AS date_value FROM stg_order_reviews WHERE review_creation_date IS NOT NULL
)
SELECT
    CAST(strftime('%Y%m%d', date_value) AS INTEGER) AS date_key,
    date_value AS full_date,
    CAST(strftime('%d', date_value) AS INTEGER) AS day,
    CAST(strftime('%m', date_value) AS INTEGER) AS month,
    CAST(strftime('%Y', date_value) AS INTEGER) AS year,
    CAST(strftime('%W', date_value) AS INTEGER) AS week_of_year,
    CASE
        WHEN CAST(strftime('%m', date_value) AS INTEGER) BETWEEN 1 AND 3 THEN 1
        WHEN CAST(strftime('%m', date_value) AS INTEGER) BETWEEN 4 AND 6 THEN 2
        WHEN CAST(strftime('%m', date_value) AS INTEGER) BETWEEN 7 AND 9 THEN 3
        ELSE 4
    END AS quarter,
    strftime('%Y-%m', date_value) AS year_month
FROM all_dates
WHERE date_value IS NOT NULL;


DROP TABLE IF EXISTS dim_customer;
CREATE TABLE dim_customer AS
SELECT
    ROW_NUMBER() OVER (ORDER BY customer_id) AS customer_key,
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM stg_customers;


DROP TABLE IF EXISTS dim_seller;
CREATE TABLE dim_seller AS
SELECT
    ROW_NUMBER() OVER (ORDER BY seller_id) AS seller_key,
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
FROM stg_sellers;


DROP TABLE IF EXISTS dim_product;
CREATE TABLE dim_product AS
SELECT
    ROW_NUMBER() OVER (ORDER BY product_id) AS product_key,
    product_id,
    product_category_name,
    product_category_name_english,
    product_name_length,
    product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
FROM stg_products;


DROP TABLE IF EXISTS fact_sales;
CREATE TABLE fact_sales AS
SELECT
    ROW_NUMBER() OVER (ORDER BY oi.order_id, oi.order_item_id) AS sales_key,
    oi.order_id,
    oi.order_item_id,

    dd.date_key AS purchase_date_key,
    dc.customer_key,
    dp.product_key,
    ds.seller_key,

    o.order_status,
    o.is_delivered,
    o.is_late_delivery,
    o.has_missing_delivery_date,

    oi.price AS item_price,
    oi.freight_value,
    oi.item_total_value,

    1 AS item_count
FROM stg_order_items oi
LEFT JOIN stg_orders o
    ON oi.order_id = o.order_id
LEFT JOIN dim_date dd
    ON date(o.order_purchase_timestamp) = dd.full_date
LEFT JOIN dim_customer dc
    ON o.customer_id = dc.customer_id
LEFT JOIN dim_product dp
    ON oi.product_id = dp.product_id
LEFT JOIN dim_seller ds
    ON oi.seller_id = ds.seller_id;


DROP TABLE IF EXISTS fact_delivery;
CREATE TABLE fact_delivery AS
SELECT
    ROW_NUMBER() OVER (ORDER BY o.order_id) AS delivery_key,
    o.order_id,

    dc.customer_key,
    purchase_date.date_key AS purchase_date_key,
    approved_date.date_key AS approved_date_key,
    carrier_date.date_key AS carrier_delivery_date_key,
    customer_delivery_date.date_key AS customer_delivery_date_key,
    estimated_date.date_key AS estimated_delivery_date_key,

    o.order_status,
    o.is_delivered,
    o.is_late_delivery,
    o.has_missing_delivery_date,
    o.delivery_days
FROM stg_orders o
LEFT JOIN dim_customer dc
    ON o.customer_id = dc.customer_id
LEFT JOIN dim_date purchase_date
    ON date(o.order_purchase_timestamp) = purchase_date.full_date
LEFT JOIN dim_date approved_date
    ON date(o.order_approved_at) = approved_date.full_date
LEFT JOIN dim_date carrier_date
    ON date(o.order_delivered_carrier_date) = carrier_date.full_date
LEFT JOIN dim_date customer_delivery_date
    ON date(o.order_delivered_customer_date) = customer_delivery_date.full_date
LEFT JOIN dim_date estimated_date
    ON date(o.order_estimated_delivery_date) = estimated_date.full_date;


DROP TABLE IF EXISTS fact_payments;
CREATE TABLE fact_payments AS
SELECT
    ROW_NUMBER() OVER (ORDER BY p.order_id, p.payment_sequential) AS payment_key,
    p.order_id,
    p.payment_sequential,
    p.payment_type,
    p.payment_installments,
    p.payment_value
FROM stg_order_payments p;


DROP TABLE IF EXISTS fact_reviews;
CREATE TABLE fact_reviews AS
SELECT
    ROW_NUMBER() OVER (ORDER BY r.review_id, r.order_id) AS review_key,
    r.review_id,
    r.order_id,
    r.review_score,
    r.has_review_comment,
    review_date.date_key AS review_creation_date_key,
    answer_date.date_key AS review_answer_date_key
FROM stg_order_reviews r
LEFT JOIN dim_date review_date
    ON date(r.review_creation_date) = review_date.full_date
LEFT JOIN dim_date answer_date
    ON date(r.review_answer_timestamp) = answer_date.full_date;