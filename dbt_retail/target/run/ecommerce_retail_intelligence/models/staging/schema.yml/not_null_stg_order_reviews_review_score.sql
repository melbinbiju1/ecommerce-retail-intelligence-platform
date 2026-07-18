
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    



select review_score
from main."stg_order_reviews"
where review_score is null



  
  
      
    ) dbt_internal_test