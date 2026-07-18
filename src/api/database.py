from pathlib import Path
import sys
from sqlalchemy import text
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine
from src.api.logging_config import api_logger


def fetch_one(query: str) -> dict:
    try:
        engine = get_engine()

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
        engine = get_engine()

        if limit is not None:
            query = f"{query} LIMIT {limit}"

        with engine.begin() as connection:
            result_df = pd.read_sql(text(query), connection)

        return result_df.to_dict(orient="records")

    except Exception as error:
        api_logger.exception(f"Database fetch_all failed: {error}")
        raise


def check_database_connection() -> bool:
    try:
        engine = get_engine()

        with engine.begin() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception as error:
        api_logger.exception(f"Database connection check failed: {error}")
        return False


def check_database_object_exists(object_name: str) -> bool:
    try:
        engine = get_engine()

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