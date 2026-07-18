
  
    
    
    create  table main."stg_geolocation"
    as
        

SELECT
    geolocation_zip_code_prefix,
    AVG(CAST(geolocation_lat AS REAL)) AS geolocation_lat,
    AVG(CAST(geolocation_lng AS REAL)) AS geolocation_lng,
    LOWER(TRIM(geolocation_city)) AS geolocation_city,
    UPPER(TRIM(geolocation_state)) AS geolocation_state,
    COUNT(*) AS source_row_count
FROM main."raw_geolocation"
GROUP BY
    geolocation_zip_code_prefix,
    LOWER(TRIM(geolocation_city)),
    UPPER(TRIM(geolocation_state))

  