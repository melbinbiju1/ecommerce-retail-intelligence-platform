DROP TABLE IF EXISTS ops_daily_metrics;

CREATE TABLE ops_daily_metrics AS
WITH daily_sales AS (
    SELECT
        dd.full_date AS metric_date,
        COUNT(DISTINCT fs.order_id) AS total_orders,
        COUNT(*) AS total_order_items,
        ROUND(SUM(fs.item_total_value), 2) AS total_revenue,
        ROUND(SUM(fs.item_price), 2) AS product_revenue,
        ROUND(SUM(fs.freight_value), 2) AS freight_revenue,
        ROUND(SUM(fs.item_total_value) / COUNT(DISTINCT fs.order_id), 2) AS avg_order_value
    FROM fact_sales fs
    LEFT JOIN dim_date dd
        ON fs.purchase_date_key = dd.date_key
    WHERE dd.full_date IS NOT NULL
    GROUP BY dd.full_date
),

daily_delivery AS (
    SELECT
        purchase_date.full_date AS metric_date,
        COUNT(DISTINCT fd.order_id) AS delivery_order_count,
        SUM(fd.is_delivered) AS delivered_orders,
        SUM(fd.is_late_delivery) AS late_delivery_orders,
        ROUND(
            100.0 * SUM(fd.is_late_delivery) / NULLIF(COUNT(DISTINCT fd.order_id), 0),
            2
        ) AS late_delivery_rate,
        SUM(
            CASE
                WHEN fd.order_status = 'canceled' THEN 1
                ELSE 0
            END
        ) AS cancelled_orders,
        ROUND(
            100.0 * SUM(
                CASE
                    WHEN fd.order_status = 'canceled' THEN 1
                    ELSE 0
                END
            ) / NULLIF(COUNT(DISTINCT fd.order_id), 0),
            2
        ) AS cancelled_order_rate,
        ROUND(AVG(fd.delivery_days), 2) AS avg_delivery_days
    FROM fact_delivery fd
    LEFT JOIN dim_date purchase_date
        ON fd.purchase_date_key = purchase_date.date_key
    WHERE purchase_date.full_date IS NOT NULL
    GROUP BY purchase_date.full_date
),

daily_reviews AS (
    SELECT
        review_date.full_date AS metric_date,
        COUNT(fr.review_id) AS total_reviews,
        ROUND(AVG(fr.review_score), 2) AS avg_review_score,
        SUM(
            CASE
                WHEN fr.review_score <= 2 THEN 1
                ELSE 0
            END
        ) AS low_review_count,
        ROUND(
            100.0 * SUM(
                CASE
                    WHEN fr.review_score <= 2 THEN 1
                    ELSE 0
                END
            ) / NULLIF(COUNT(fr.review_id), 0),
            2
        ) AS low_review_rate
    FROM fact_reviews fr
    LEFT JOIN dim_date review_date
        ON fr.review_creation_date_key = review_date.date_key
    WHERE review_date.full_date IS NOT NULL
    GROUP BY review_date.full_date
)

SELECT
    ds.metric_date,
    ds.total_orders,
    ds.total_order_items,
    ds.total_revenue,
    ds.product_revenue,
    ds.freight_revenue,
    ds.avg_order_value,

    COALESCE(dd.delivered_orders, 0) AS delivered_orders,
    COALESCE(dd.late_delivery_orders, 0) AS late_delivery_orders,
    COALESCE(dd.late_delivery_rate, 0) AS late_delivery_rate,
    COALESCE(dd.cancelled_orders, 0) AS cancelled_orders,
    COALESCE(dd.cancelled_order_rate, 0) AS cancelled_order_rate,
    dd.avg_delivery_days,

    COALESCE(dr.total_reviews, 0) AS total_reviews,
    dr.avg_review_score,
    COALESCE(dr.low_review_count, 0) AS low_review_count,
    COALESCE(dr.low_review_rate, 0) AS low_review_rate,

    datetime('now') AS created_at
FROM daily_sales ds
LEFT JOIN daily_delivery dd
    ON ds.metric_date = dd.metric_date
LEFT JOIN daily_reviews dr
    ON ds.metric_date = dr.metric_date;


DROP TABLE IF EXISTS ops_seller_metrics;

CREATE TABLE ops_seller_metrics AS
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
FROM fact_sales fs
LEFT JOIN dim_seller ds
    ON fs.seller_key = ds.seller_key
LEFT JOIN fact_reviews fr
    ON fs.order_id = fr.order_id
GROUP BY
    ds.seller_id,
    ds.seller_city,
    ds.seller_state;


DROP TABLE IF EXISTS ops_category_metrics;

CREATE TABLE ops_category_metrics AS
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
FROM fact_sales fs
LEFT JOIN dim_product dp
    ON fs.product_key = dp.product_key
LEFT JOIN fact_reviews fr
    ON fs.order_id = fr.order_id
GROUP BY
    dp.product_category_name_english;