
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    



select product_category_name
from main."stg_product_category_translation"
where product_category_name is null



  
  
      
    ) dbt_internal_test