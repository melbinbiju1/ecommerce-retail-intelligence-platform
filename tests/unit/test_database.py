from src.api.database import check_database_connection, check_database_object_exists


IMPORTANT_OBJECTS = [
    "fact_sales",
    "dim_customer",
    "dim_seller",
    "vw_executive_summary",
    "vw_monthly_sales",
    "vw_operational_alert_summary",
    "vw_operational_alerts_by_type",
    "vw_high_risk_sellers",
    "vw_high_risk_categories",
]


def test_database_connection():
    assert check_database_connection() is True


def test_important_database_objects_exist():
    missing_objects = [
        object_name
        for object_name in IMPORTANT_OBJECTS
        if not check_database_object_exists(object_name)
    ]

    assert missing_objects == []