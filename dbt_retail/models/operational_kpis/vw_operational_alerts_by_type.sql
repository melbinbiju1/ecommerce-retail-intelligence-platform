{{ config(materialized='view') }}

SELECT
    alert_type,
    business_area,
    severity,
    COUNT(*) AS alert_count,
    ROUND(AVG(actual_value), 2) AS avg_actual_value,
    ROUND(AVG(expected_value), 2) AS avg_expected_value,
    ROUND(AVG(difference_percentage), 2) AS avg_difference_percentage
FROM {{ source('operations_external', 'ops_anomaly_alerts') }}
GROUP BY
    alert_type,
    business_area,
    severity
ORDER BY
    alert_count DESC