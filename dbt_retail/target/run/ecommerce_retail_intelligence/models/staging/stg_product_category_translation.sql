
  
    
    
    create  table main."stg_product_category_translation"
    as
        

SELECT
    LOWER(TRIM(product_category_name)) AS product_category_name,
    LOWER(TRIM(product_category_name_english)) AS product_category_name_english,
    _source_file,
    _loaded_at
FROM main."raw_product_category_translation"

  