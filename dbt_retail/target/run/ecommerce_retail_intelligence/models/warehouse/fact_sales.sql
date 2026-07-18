
  
    
    
    create  table main."fact_sales"
    as
        

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
FROM main."stg_order_items" oi
LEFT JOIN main."stg_orders" o
    ON oi.order_id = o.order_id
LEFT JOIN main."dim_date" dd
    ON date(o.order_purchase_timestamp) = dd.full_date
LEFT JOIN main."dim_customer" dc
    ON o.customer_id = dc.customer_id
LEFT JOIN main."dim_product" dp
    ON oi.product_id = dp.product_id
LEFT JOIN main."dim_seller" ds
    ON oi.seller_id = ds.seller_id

  