{{ config(materialized='table') }}

SELECT
    customer_id,
    customer_unique_id,
    CAST(customer_zip_code_prefix AS INTEGER) AS customer_zip_code_prefix,
    LOWER(TRIM(customer_city)) AS customer_city,
    UPPER(TRIM(customer_state)) AS customer_state,
    _source_file,
    _loaded_at
FROM {{ source('raw', 'raw_customers') }}