
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        seller_risk_level as value_field,
        count(*) as n_records

    from main."ops_seller_metrics"
    group by seller_risk_level

)

select *
from all_values
where value_field not in (
    'low','medium','high'
)



  
  
      
    ) dbt_internal_test