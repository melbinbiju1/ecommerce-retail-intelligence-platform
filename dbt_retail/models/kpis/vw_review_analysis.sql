{{ config(materialized='view') }}

SELECT
    fr.review_score,
    COUNT(*) AS review_count,
    SUM(fr.has_review_comment) AS reviews_with_comment,
    ROUND(AVG(fd.delivery_days), 2) AS avg_delivery_days,
    SUM(fd.is_late_delivery) AS late_delivery_orders
FROM {{ ref('fact_reviews') }} fr
LEFT JOIN {{ ref('fact_delivery') }} fd
    ON fr.order_id = fd.order_id
GROUP BY
    fr.review_score
ORDER BY
    fr.review_score