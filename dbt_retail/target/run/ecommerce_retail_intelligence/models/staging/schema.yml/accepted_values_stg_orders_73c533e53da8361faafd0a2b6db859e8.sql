
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        order_status as value_field,
        count(*) as n_records

    from main."stg_orders"
    group by order_status

)

select *
from all_values
where value_field not in (
    'delivered','shipped','canceled','unavailable','invoiced','processing','created','approved'
)



  
  
      
    ) dbt_internal_test