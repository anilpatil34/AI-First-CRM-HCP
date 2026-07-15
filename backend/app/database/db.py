"""
Database engine and table creation.
Handles SQLite and PostgreSQL connection configuration.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.database.base import Base

settings = get_settings()

# Engine configuration
connect_args = {}
if settings.is_sqlite:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# Enable WAL mode for SQLite (better concurrent read performance)
if settings.is_sqlite:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def create_tables():
    """Create all database tables if they don't exist."""
    # Import models to register them with Base metadata
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=engine)


def get_engine():
    """Get the database engine instance."""
    return engine
