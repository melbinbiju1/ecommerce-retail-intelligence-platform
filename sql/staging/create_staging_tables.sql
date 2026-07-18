DROP TABLE IF EXISTS stg_customers;
CREATE TABLE stg_customers AS
SELECT
    customer_id,
    customer_unique_id,
    CAST(customer_zip_code_prefix AS INTEGER) AS customer_zip_code_prefix,
    LOWER(TRIM(customer_city)) AS customer_city,
    UPPER(TRIM(customer_state)) AS customer_state,
    _source_file,
    _loaded_at
FROM raw_customers;


DROP TABLE IF EXISTS stg_sellers;
CREATE TABLE stg_sellers AS
SELECT
    seller_id,
    CAST(seller_zip_code_prefix AS INTEGER) AS seller_zip_code_prefix,
    LOWER(TRIM(seller_city)) AS seller_city,
    UPPER(TRIM(seller_state)) AS seller_state,
    _source_file,
    _loaded_at
FROM raw_sellers;


DROP TABLE IF EXISTS stg_product_category_translation;
CREATE TABLE stg_product_category_translation AS
SELECT
    LOWER(TRIM(product_category_name)) AS product_category_name,
    LOWER(TRIM(product_category_name_english)) AS product_category_name_english,
    _source_file,
    _loaded_at
FROM raw_product_category_translation;


DROP TABLE IF EXISTS stg_products;
CREATE TABLE stg_products AS
SELECT
    p.product_id,
    LOWER(TRIM(COALESCE(p.product_category_name, 'unknown'))) AS product_category_name,
    LOWER(TRIM(COALESCE(t.product_category_name_english, p.product_category_name, 'unknown'))) AS product_category_name_english,
    CAST(p.product_name_lenght AS INTEGER) AS product_name_length,
    CAST(p.product_description_lenght AS INTEGER) AS product_description_length,
    CAST(p.product_photos_qty AS INTEGER) AS product_photos_qty,
    CAST(p.product_weight_g AS REAL) AS product_weight_g,
    CAST(p.product_length_cm AS REAL) AS product_length_cm,
    CAST(p.product_height_cm AS REAL) AS product_height_cm,
    CAST(p.product_width_cm AS REAL) AS product_width_cm,
    p._source_file,
    p._loaded_at
FROM raw_products p
LEFT JOIN stg_product_category_translation t
    ON LOWER(TRIM(p.product_category_name)) = t.product_category_name;


DROP TABLE IF EXISTS stg_orders;
CREATE TABLE stg_orders AS
SELECT
    order_id,
    customer_id,
    LOWER(TRIM(order_status)) AS order_status,
    datetime(order_purchase_timestamp) AS order_purchase_timestamp,
    datetime(order_approved_at) AS order_approved_at,
    datetime(order_delivered_carrier_date) AS order_delivered_carrier_date,
    datetime(order_delivered_customer_date) AS order_delivered_customer_date,
    datetime(order_estimated_delivery_date) AS order_estimated_delivery_date,

    CASE
        WHEN order_status = 'delivered' THEN 1
        ELSE 0
    END AS is_delivered,

    CASE
        WHEN order_status = 'delivered'
         AND order_delivered_customer_date IS NULL THEN 1
        ELSE 0
    END AS has_missing_delivery_date,

    CASE
        WHEN order_delivered_customer_date IS NOT NULL
         AND order_estimated_delivery_date IS NOT NULL
         AND datetime(order_delivered_customer_date) > datetime(order_estimated_delivery_date)
        THEN 1
        ELSE 0
    END AS is_late_delivery,

    CASE
        WHEN order_delivered_customer_date IS NOT NULL
         AND order_purchase_timestamp IS NOT NULL
        THEN CAST(
            julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)
            AS INTEGER
        )
        ELSE NULL
    END AS delivery_days,

    _source_file,
    _loaded_at
FROM raw_orders;


DROP TABLE IF EXISTS stg_order_items;
CREATE TABLE stg_order_items AS
SELECT
    order_id,
    CAST(order_item_id AS INTEGER) AS order_item_id,
    product_id,
    seller_id,
    datetime(shipping_limit_date) AS shipping_limit_date,
    CAST(price AS REAL) AS price,
    CAST(freight_value AS REAL) AS freight_value,
    CAST(price + freight_value AS REAL) AS item_total_value,
    _source_file,
    _loaded_at
FROM raw_order_items;


DROP TABLE IF EXISTS stg_order_payments;
CREATE TABLE stg_order_payments AS
SELECT
    order_id,
    CAST(payment_sequential AS INTEGER) AS payment_sequential,
    LOWER(TRIM(payment_type)) AS payment_type,
    CAST(payment_installments AS INTEGER) AS payment_installments,
    CAST(payment_value AS REAL) AS payment_value,
    _source_file,
    _loaded_at
FROM raw_order_payments;


DROP TABLE IF EXISTS stg_order_reviews;
CREATE TABLE stg_order_reviews AS
SELECT
    review_id,
    order_id,
    CAST(review_score AS INTEGER) AS review_score,
    review_comment_title,
    review_comment_message,
    datetime(review_creation_date) AS review_creation_date,
    datetime(review_answer_timestamp) AS review_answer_timestamp,

    CASE
        WHEN review_comment_message IS NULL OR TRIM(review_comment_message) = ''
        THEN 0
        ELSE 1
    END AS has_review_comment,

    _source_file,
    _loaded_at
FROM raw_order_reviews;


DROP TABLE IF EXISTS stg_geolocation;
CREATE TABLE stg_geolocation AS
SELECT
    geolocation_zip_code_prefix,
    AVG(CAST(geolocation_lat AS REAL)) AS geolocation_lat,
    AVG(CAST(geolocation_lng AS REAL)) AS geolocation_lng,
    LOWER(TRIM(geolocation_city)) AS geolocation_city,
    UPPER(TRIM(geolocation_state)) AS geolocation_state,
    COUNT(*) AS source_row_count
FROM raw_geolocation
GROUP BY
    geolocation_zip_code_prefix,
    LOWER(TRIM(geolocation_city)),
    UPPER(TRIM(geolocation_state));