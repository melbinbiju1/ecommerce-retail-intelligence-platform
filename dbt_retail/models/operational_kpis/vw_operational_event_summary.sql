{{ config(materialized='view') }}

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
FROM {{ source('operations_external', 'ops_event_log') }}