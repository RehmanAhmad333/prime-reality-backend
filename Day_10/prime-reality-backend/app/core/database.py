# prime-reality-backend/core/database.py

import os
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError, OperationalError

load_dotenv()

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/primerealty"
)

if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL environment variable is not set.")

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,          # max persistent connections in pool
        max_overflow=20,       # extra connections allowed beyond pool_size
        connect_args={"connect_timeout": 10},  # fail fast if DB unreachable
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base = declarative_base()

    logger.info("Database engine initialized successfully")

except OperationalError as e:
    logger.exception("Operational error during database engine initialization")
    raise

except SQLAlchemyError as e:
    logger.exception("SQLAlchemy error during database engine initialization")
    raise

except Exception as e:
    logger.exception("Unexpected error during database engine initialization")
    raise


# Startup connection test
def test_database_connection() -> None:
    """Verifies the database is reachable. Raises on failure."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")

    except OperationalError:
        logger.exception("Operational error: database unreachable or credentials invalid")
        raise

    except SQLAlchemyError:
        logger.exception("SQLAlchemy error during connection test")
        raise

    except Exception:
        logger.exception("Unexpected error during database connection test")
        raise


def get_db():
    """
    FastAPI dependency that yields a SQLAlchemy session.
    Rolls back on any error, always closes the session.
    """
    db = SessionLocal()

    try:
        yield db

    except SQLAlchemyError:
        logger.exception("Database session error — rolling back")
        db.rollback()
        raise

    except Exception:
        logger.exception("Unexpected error in database session — rolling back")
        db.rollback()
        raise

    finally:
        db.close()