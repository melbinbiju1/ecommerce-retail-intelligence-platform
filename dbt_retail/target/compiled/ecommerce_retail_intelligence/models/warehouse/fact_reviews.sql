

SELECT
    ROW_NUMBER() OVER (ORDER BY r.review_id, r.order_id) AS review_key,
    r.review_id,
    r.order_id,
    r.review_score,
    r.has_review_comment,
    review_date.date_key AS review_creation_date_key,
    answer_date.date_key AS review_answer_date_key
FROM main."stg_order_reviews" r
LEFT JOIN main."dim_date" review_date
    ON date(r.review_creation_date) = review_date.full_date
LEFT JOIN main."dim_date" answer_date
    ON date(r.review_answer_timestamp) = answer_date.full_date