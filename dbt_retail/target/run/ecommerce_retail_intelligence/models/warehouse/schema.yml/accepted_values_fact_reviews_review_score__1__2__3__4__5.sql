
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        review_score as value_field,
        count(*) as n_records

    from main."fact_reviews"
    group by review_score

)

select *
from all_values
where value_field not in (
    '1','2','3','4','5'
)



  
  
      
    ) dbt_internal_test