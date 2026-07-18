
  
    
    
    create  table main."fact_payments"
    as
        

SELECT
    ROW_NUMBER() OVER (ORDER BY p.order_id, p.payment_sequential) AS payment_key,
    p.order_id,
    p.payment_sequential,
    p.payment_type,
    p.payment_installments,
    p.payment_value
FROM main."stg_order_payments" p

  