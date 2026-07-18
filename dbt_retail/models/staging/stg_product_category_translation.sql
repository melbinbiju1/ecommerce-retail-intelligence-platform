{{ config(materialized='table') }}

SELECT
    LOWER(TRIM(product_category_name)) AS product_category_name,
    LOWER(TRIM(product_category_name_english)) AS product_category_name_english,
    _source_file,
    _loaded_at
FROM {{ source('raw', 'raw_product_category_translation') }}