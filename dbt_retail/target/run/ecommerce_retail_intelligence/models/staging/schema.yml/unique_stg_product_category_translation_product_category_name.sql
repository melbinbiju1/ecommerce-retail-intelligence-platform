
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    

select
    product_category_name as unique_field,
    count(*) as n_records

from main."stg_product_category_translation"
where product_category_name is not null
group by product_category_name
having count(*) > 1



  
  
      
    ) dbt_internal_test