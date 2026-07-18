
  
    
    
    create  table main."stg_order_reviews"
    as
        

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
FROM main."raw_order_reviews"

  