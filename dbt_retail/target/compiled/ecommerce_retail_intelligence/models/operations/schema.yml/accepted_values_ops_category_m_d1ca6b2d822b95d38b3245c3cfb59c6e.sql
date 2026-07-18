
    
    

with all_values as (

    select
        category_risk_level as value_field,
        count(*) as n_records

    from main."ops_category_metrics"
    group by category_risk_level

)

select *
from all_values
where value_field not in (
    'low','medium','high'
)


