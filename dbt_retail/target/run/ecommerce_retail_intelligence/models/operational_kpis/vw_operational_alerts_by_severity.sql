
    
    create view main."vw_operational_alerts_by_severity" as
    

SELECT
    severity,
    COUNT(*) AS alert_count,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM main."ops_anomaly_alerts"),
        2
    ) AS alert_percentage
FROM main."ops_anomaly_alerts"
GROUP BY
    severity
ORDER BY
    CASE severity
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
        ELSE 5
    END;