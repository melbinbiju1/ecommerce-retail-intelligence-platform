
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    

select
    product_category_name_english as unique_field,
    count(*) as n_records

from main."ops_category_metrics"
where product_category_name_english is not null
group by product_category_name_english
having count(*) > 1



  
  
      
    ) dbt_internal_test