

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
FROM main."stg_orders" o
LEFT JOIN main."dim_customer" dc
    ON o.customer_id = dc.customer_id
LEFT JOIN main."dim_date" purchase_date
    ON date(o.order_purchase_timestamp) = purchase_date.full_date
LEFT JOIN main."dim_date" approved_date
    ON date(o.order_approved_at) = approved_date.full_date
LEFT JOIN main."dim_date" carrier_date
    ON date(o.order_delivered_carrier_date) = carrier_date.full_date
LEFT JOIN main."dim_date" customer_delivery_date
    ON date(o.order_delivered_customer_date) = customer_delivery_date.full_date
LEFT JOIN main."dim_date" estimated_date
    ON date(o.order_estimated_delivery_date) = estimated_date.full_date