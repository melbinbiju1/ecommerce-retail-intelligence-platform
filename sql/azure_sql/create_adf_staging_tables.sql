IF OBJECT_ID('dbo.adf_stg_orders_raw', 'U') IS NOT NULL
    DROP TABLE dbo.adf_stg_orders_raw;
GO

CREATE TABLE dbo.adf_stg_orders_raw (
    order_id NVARCHAR(100) NULL,
    customer_id NVARCHAR(100) NULL,
    order_status NVARCHAR(50) NULL,
    order_purchase_timestamp NVARCHAR(50) NULL,
    order_approved_at NVARCHAR(50) NULL,
    order_delivered_carrier_date NVARCHAR(50) NULL,
    order_delivered_customer_date NVARCHAR(50) NULL,
    order_estimated_delivery_date NVARCHAR(50) NULL
);
GO