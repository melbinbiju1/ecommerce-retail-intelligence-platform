from pathlib import Path
from sqlalchemy import create_engine


DATABASE_PATH = Path("retail_intelligence.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


def get_engine():
    """
    Create and return a SQLAlchemy database engine.

    For local development, this project uses SQLite.
    Later, this same pattern will be adapted for Azure SQL Database.
    """
    engine = create_engine(DATABASE_URL)
    return engine