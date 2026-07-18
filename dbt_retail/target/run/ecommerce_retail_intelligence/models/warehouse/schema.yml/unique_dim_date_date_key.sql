
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    

select
    date_key as unique_field,
    count(*) as n_records

from main."dim_date"
where date_key is not null
group by date_key
having count(*) > 1



  
  
      
    ) dbt_internal_test