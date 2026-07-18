
    select
      count(*) as failures,
      case when count(*) != 0
        then 'true' else 'false' end as should_warn,
      case when count(*) != 0
        then 'true' else 'false' end as should_error
    from (
      
    
  
    
    

select
    metric_date as unique_field,
    count(*) as n_records

from main."ops_daily_metrics"
where metric_date is not null
group by metric_date
having count(*) > 1



  
  
      
    ) dbt_internal_test