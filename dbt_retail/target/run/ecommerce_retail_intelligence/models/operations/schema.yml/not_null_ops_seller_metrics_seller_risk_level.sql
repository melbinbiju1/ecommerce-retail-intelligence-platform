
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    



select seller_risk_level
from main."ops_seller_metrics"
where seller_risk_level is null



  
  
      
    ) dbt_internal_test