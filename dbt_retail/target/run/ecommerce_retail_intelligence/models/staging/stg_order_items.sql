
  
    
    
    create  table main."stg_order_items"
    as
        

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
FROM main."raw_order_items"

  