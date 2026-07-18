{{ config(materialized='view') }}

SELECT
    'anomaly_alerts' AS risk_source,
    business_area,
    severity,
    COUNT(*) AS risk_count
FROM {{ source('operations_external', 'ops_anomaly_alerts') }}
GROUP BY
    business_area,
    severity

UNION ALL

SELECT
    'event_records' AS risk_source,
    business_area,
    severity,
    COUNT(*) AS risk_count
FROM {{ source('operations_external', 'ops_event_records') }}
GROUP BY
    business_area,
    severity