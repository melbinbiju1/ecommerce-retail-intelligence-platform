

SELECT
    alert_id,
    alert_date,
    alert_type,
    severity,
    business_area,
    entity_id,
    entity_name,
    metric_name,
    actual_value,
    expected_value,
    difference_value,
    difference_percentage,
    alert_description,
    recommended_action,
    created_at
FROM main."ops_anomaly_alerts"
ORDER BY
    CASE severity
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
        ELSE 5
    END,
    alert_id DESC