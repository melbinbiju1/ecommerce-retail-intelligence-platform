from pathlib import Path
import os
import sys

import pandas as pd
from sqlalchemy import text


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine as get_sqlite_engine  # noqa: E402
from src.cloud.azure_sql_database import get_azure_sql_engine  # noqa: E402
from src.api.logging_config import api_logger  # noqa: E402


def get_api_database_engine():
    """
    Returns the correct database engine for the API.

    Local development:
        APP_ENV=local or missing -> SQLite

    Azure deployment:
        APP_ENV=azure -> Azure SQL Database
    """
    app_env = os.getenv("APP_ENV", "local").lower().strip()

    if app_env == "azure":
        return get_azure_sql_engine()

    return get_sqlite_engine()


def is_azure_sql_mode() -> bool:
    """
    Checks whether the API is running in Azure SQL mode.
    """
    return os.getenv("APP_ENV", "local").lower().strip() == "azure"


def fetch_one(query: str) -> dict:
    try:
        engine = get_api_database_engine()

        with engine.begin() as connection:
            result_df = pd.read_sql(text(query), connection)

        if result_df.empty:
            return {}

        return result_df.iloc[0].to_dict()

    except Exception as error:
        api_logger.exception(f"Database fetch_one failed: {error}")
        raise


def fetch_all(query: str, limit: int | None = None) -> list[dict]:
    try:
        engine = get_api_database_engine()

        # We avoid appending database-specific LIMIT syntax here because:
        # - SQLite supports LIMIT
        # - Azure SQL uses TOP/OFFSET instead of LIMIT
        #
        # For portfolio API workloads, reading the query result and then limiting
        # in pandas keeps the same API code working in both modes.
        with engine.begin() as connection:
            result_df = pd.read_sql(text(query), connection)

        if limit is not None:
            result_df = result_df.head(limit)

        return result_df.to_dict(orient="records")

    except Exception as error:
        api_logger.exception(f"Database fetch_all failed: {error}")
        raise


def check_database_connection() -> bool:
    try:
        engine = get_api_database_engine()

        with engine.begin() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception as error:
        api_logger.exception(f"Database connection check failed: {error}")
        return False


def check_database_object_exists(object_name: str) -> bool:
    try:
        engine = get_api_database_engine()

        if is_azure_sql_mode():
            query = """
            SELECT object_id
            FROM sys.objects
            WHERE name = :object_name
              AND type IN ('U', 'V')
            """
        else:
            query = """
            SELECT name
            FROM sqlite_master
            WHERE name = :object_name
              AND type IN ('table', 'view')
            """

        with engine.begin() as connection:
            result_df = pd.read_sql(
                text(query),
                connection,
                params={"object_name": object_name},
            )

        return not result_df.empty

    except Exception as error:
        api_logger.exception(f"Database object check failed for {object_name}: {error}")
        return False