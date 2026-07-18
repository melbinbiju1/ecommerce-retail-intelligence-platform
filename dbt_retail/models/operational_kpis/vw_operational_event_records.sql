{{ config(materialized='view') }}

SELECT
    event_id,
    event_timestamp,
    event_type,
    severity,
    business_area,
    entity_id,
    entity_name,
    metric_name,
    actual_value,
    expected_value,
    event_description,
    recommended_action,
    source_system,
    file_name,
    processed_at
FROM {{ source('operations_external', 'ops_event_records') }}
ORDER BY
    processed_at DESC