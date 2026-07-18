{{ config(materialized='table') }}

SELECT
    p.product_id,
    LOWER(TRIM(COALESCE(p.product_category_name, 'unknown'))) AS product_category_name,
    LOWER(TRIM(COALESCE(t.product_category_name_english, p.product_category_name, 'unknown'))) AS product_category_name_english,
    CAST(p.product_name_lenght AS INTEGER) AS product_name_length,
    CAST(p.product_description_lenght AS INTEGER) AS product_description_length,
    CAST(p.product_photos_qty AS INTEGER) AS product_photos_qty,
    CAST(p.product_weight_g AS REAL) AS product_weight_g,
    CAST(p.product_length_cm AS REAL) AS product_length_cm,
    CAST(p.product_height_cm AS REAL) AS product_height_cm,
    CAST(p.product_width_cm AS REAL) AS product_width_cm,
    p._source_file,
    p._loaded_at
FROM {{ source('raw', 'raw_products') }} p
LEFT JOIN {{ ref('stg_product_category_translation') }} t
    ON LOWER(TRIM(p.product_category_name)) = t.product_category_name