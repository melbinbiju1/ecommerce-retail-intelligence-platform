from pathlib import Path
from urllib.parse import quote_plus
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_azure_sql_config() -> dict:
    """
    Load Azure SQL Database configuration from the local .env file.
    """
    load_dotenv(PROJECT_ROOT / ".env")

    server = os.getenv("AZURE_SQL_SERVER")
    database = os.getenv("AZURE_SQL_DATABASE")
    username = os.getenv("AZURE_SQL_USERNAME")
    password = os.getenv("AZURE_SQL_PASSWORD")
    driver = os.getenv("AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server")

    missing_values = []

    for key, value in {
        "AZURE_SQL_SERVER": server,
        "AZURE_SQL_DATABASE": database,
        "AZURE_SQL_USERNAME": username,
        "AZURE_SQL_PASSWORD": password,
        "AZURE_SQL_DRIVER": driver,
    }.items():
        if not value:
            missing_values.append(key)

    if missing_values:
        raise ValueError(
            "Missing Azure SQL environment variables: "
            + ", ".join(missing_values)
        )

    return {
        "server": server,
        "database": database,
        "username": username,
        "password": password,
        "driver": driver,
    }


def build_azure_sql_connection_string() -> str:
    """
    Build a SQLAlchemy connection string for Azure SQL Database using pyodbc.
    """
    config = load_azure_sql_config()

    odbc_connection = (
        f"DRIVER={{{config['driver']}}};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"UID={config['username']};"
        f"PWD={config['password']};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    return f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_connection)}"


def get_azure_sql_engine() -> Engine:
    """
    Create a SQLAlchemy engine for Azure SQL Database.
    """
    connection_string = build_azure_sql_connection_string()

    return create_engine(
        connection_string,
        fast_executemany=True,
        pool_pre_ping=True,
    )


def test_azure_sql_connection() -> dict:
    """
    Test Azure SQL Database connectivity.
    """
    engine = get_azure_sql_engine()

    with engine.connect() as connection:
        result = connection.execute(text("SELECT @@VERSION AS sql_version"))
        row = result.fetchone()

    return {
        "connection_status": "success",
        "sql_version": row[0] if row else None,
    }