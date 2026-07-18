{{ config(materialized='view') }}

SELECT
    COUNT(*) AS total_alerts,
    SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) AS critical_alerts,
    SUM(CASE WHEN severity = 'high' THEN 1 ELSE 0 END) AS high_alerts,
    SUM(CASE WHEN severity = 'medium' THEN 1 ELSE 0 END) AS medium_alerts,
    SUM(CASE WHEN severity = 'low' THEN 1 ELSE 0 END) AS low_alerts,
    COUNT(DISTINCT alert_type) AS alert_types,
    COUNT(DISTINCT business_area) AS business_areas_affected
FROM {{ source('operations_external', 'ops_anomaly_alerts') }}