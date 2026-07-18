
  
    
    
    create  table main."stg_sellers"
    as
        

SELECT
    seller_id,
    CAST(seller_zip_code_prefix AS INTEGER) AS seller_zip_code_prefix,
    LOWER(TRIM(seller_city)) AS seller_city,
    UPPER(TRIM(seller_state)) AS seller_state,
    _source_file,
    _loaded_at
FROM main."raw_sellers"

  