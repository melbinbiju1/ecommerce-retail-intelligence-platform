DROP VIEW IF EXISTS vw_operational_alert_summary;
CREATE VIEW vw_operational_alert_summary AS
SELECT
    COUNT(*) AS total_alerts,
    SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) AS critical_alerts,
    SUM(CASE WHEN severity = 'high' THEN 1 ELSE 0 END) AS high_alerts,
    SUM(CASE WHEN severity = 'medium' THEN 1 ELSE 0 END) AS medium_alerts,
    SUM(CASE WHEN severity = 'low' THEN 1 ELSE 0 END) AS low_alerts,
    COUNT(DISTINCT alert_type) AS alert_types,
    COUNT(DISTINCT business_area) AS business_areas_affected
FROM ops_anomaly_alerts;


DROP VIEW IF EXISTS vw_operational_alerts_by_type;
CREATE VIEW vw_operational_alerts_by_type AS
SELECT
    alert_type,
    business_area,
    severity,
    COUNT(*) AS alert_count,
    ROUND(AVG(actual_value), 2) AS avg_actual_value,
    ROUND(AVG(expected_value), 2) AS avg_expected_value,
    ROUND(AVG(difference_percentage), 2) AS avg_difference_percentage
FROM ops_anomaly_alerts
GROUP BY
    alert_type,
    business_area,
    severity
ORDER BY
    alert_count DESC;


DROP VIEW IF EXISTS vw_operational_alerts_by_severity;
CREATE VIEW vw_operational_alerts_by_severity AS
SELECT
    severity,
    COUNT(*) AS alert_count,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM ops_anomaly_alerts),
        2
    ) AS alert_percentage
FROM ops_anomaly_alerts
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


DROP VIEW IF EXISTS vw_recent_operational_alerts;
CREATE VIEW vw_recent_operational_alerts AS
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
FROM ops_anomaly_alerts
ORDER BY
    CASE severity
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
        ELSE 5
    END,
    alert_id DESC;


DROP VIEW IF EXISTS vw_high_risk_sellers;
CREATE VIEW vw_high_risk_sellers AS
SELECT
    seller_id,
    seller_city,
    seller_state,
    total_orders,
    total_items_sold,
    total_revenue,
    avg_item_value,
    late_delivery_items,
    late_delivery_rate,
    avg_review_score,
    seller_risk_level
FROM ops_seller_metrics
WHERE seller_risk_level IN ('high', 'medium')
ORDER BY
    CASE seller_risk_level
        WHEN 'high' THEN 1
        WHEN 'medium' THEN 2
        ELSE 3
    END,
    late_delivery_rate DESC,
    total_revenue DESC;


DROP VIEW IF EXISTS vw_high_risk_categories;
CREATE VIEW vw_high_risk_categories AS
SELECT
    product_category_name_english,
    total_orders,
    total_items_sold,
    total_revenue,
    avg_item_price,
    avg_review_score,
    late_delivery_items,
    late_delivery_rate,
    category_risk_level
FROM ops_category_metrics
WHERE category_risk_level IN ('high', 'medium')
ORDER BY
    CASE category_risk_level
        WHEN 'high' THEN 1
        WHEN 'medium' THEN 2
        ELSE 3
    END,
    late_delivery_rate DESC,
    total_revenue DESC;


DROP VIEW IF EXISTS vw_operational_event_summary;
CREATE VIEW vw_operational_event_summary AS
SELECT
    COUNT(*) AS total_event_files_processed,
    SUM(total_records) AS total_records_received,
    SUM(valid_records) AS total_valid_records,
    SUM(failed_records) AS total_failed_records,
    ROUND(
        100.0 * SUM(valid_records) / NULLIF(SUM(total_records), 0),
        2
    ) AS valid_record_percentage,
    ROUND(
        100.0 * SUM(failed_records) / NULLIF(SUM(total_records), 0),
        2
    ) AS failed_record_percentage,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successful_files,
    SUM(CASE WHEN status = 'PARTIAL_SUCCESS' THEN 1 ELSE 0 END) AS partial_success_files,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS failed_files
FROM ops_event_log;


DROP VIEW IF EXISTS vw_operational_event_records;
CREATE VIEW vw_operational_event_records AS
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
FROM ops_event_records
ORDER BY
    processed_at DESC;


DROP VIEW IF EXISTS vw_operational_risk_summary;
CREATE VIEW vw_operational_risk_summary AS
SELECT
    'anomaly_alerts' AS risk_source,
    business_area,
    severity,
    COUNT(*) AS risk_count
FROM ops_anomaly_alerts
GROUP BY
    business_area,
    severity

UNION ALL

SELECT
    'event_records' AS risk_source,
    business_area,
    severity,
    COUNT(*) AS risk_count
FROM ops_event_records
GROUP BY
    business_area,
    severity;