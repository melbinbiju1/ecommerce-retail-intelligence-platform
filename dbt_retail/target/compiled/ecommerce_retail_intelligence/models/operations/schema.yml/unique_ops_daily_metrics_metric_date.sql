
    
    

select
    metric_date as unique_field,
    count(*) as n_records

from main."ops_daily_metrics"
where metric_date is not null
group by metric_date
having count(*) > 1


