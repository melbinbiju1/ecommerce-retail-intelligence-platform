
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    



select seller_id
from main."stg_order_items"
where seller_id is null



  
  
      
    ) dbt_internal_test