
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    



select product_category_name_english
from main."ops_category_metrics"
where product_category_name_english is null



  
  
      
    ) dbt_internal_test