
    
    create view main."vw_operational_risk_summary" as
    

SELECT
    'anomaly_alerts' AS risk_source,
    business_area,
    severity,
    COUNT(*) AS risk_count
FROM main."ops_anomaly_alerts"
GROUP BY
    business_area,
    severity

UNION ALL

SELECT
    'event_records' AS risk_source,
    business_area,
    severity,
    COUNT(*) AS risk_count
FROM main."ops_event_records"
GROUP BY
    business_area,
    severity;