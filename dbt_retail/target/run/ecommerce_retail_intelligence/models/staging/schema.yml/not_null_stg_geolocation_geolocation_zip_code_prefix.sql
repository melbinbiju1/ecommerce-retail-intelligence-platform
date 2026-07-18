
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    



select geolocation_zip_code_prefix
from main."stg_geolocation"
where geolocation_zip_code_prefix is null



  
  
      
    ) dbt_internal_test