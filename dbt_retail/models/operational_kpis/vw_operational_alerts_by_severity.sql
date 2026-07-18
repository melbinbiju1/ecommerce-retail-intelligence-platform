{{ config(materialized='view') }}

SELECT
    severity,
    COUNT(*) AS alert_count,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM {{ source('operations_external', 'ops_anomaly_alerts') }}),
        2
    ) AS alert_percentage
FROM {{ source('operations_external', 'ops_anomaly_alerts') }}
GROUP BY
    severity
ORDER BY
    CASE severity
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
        ELSE 5
    END