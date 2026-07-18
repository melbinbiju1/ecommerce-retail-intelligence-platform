
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    



select category_risk_level
from main."ops_category_metrics"
where category_risk_level is null



  
  
      
    ) dbt_internal_test