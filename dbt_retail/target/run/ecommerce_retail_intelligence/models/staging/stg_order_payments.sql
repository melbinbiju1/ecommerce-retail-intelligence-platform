
  
    
    
    create  table main."stg_order_payments"
    as
        

SELECT
    order_id,
    CAST(payment_sequential AS INTEGER) AS payment_sequential,
    LOWER(TRIM(payment_type)) AS payment_type,
    CAST(payment_installments AS INTEGER) AS payment_installments,
    CAST(payment_value AS REAL) AS payment_value,
    _source_file,
    _loaded_at
FROM main."raw_order_payments"

  