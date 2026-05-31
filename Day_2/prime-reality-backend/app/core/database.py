# This module sets up the database connection and session management for the Prime Reality backend application. It uses SQLAlchemy for ORM and connection pooling, and includes error handling and logging for robust database interactions. The `get_db` function provides a generator for database sessions, ensuring proper cleanup after use.

import os
import logging # Importing the logging module to enable logging throughout the database module

from dotenv import load_dotenv
from sqlalchemy import create_engine, text  # Importing necessary SQLAlchemy components for creating the database engine and executing raw SQL
from sqlalchemy.orm import sessionmaker, declarative_base # Importing sessionmaker for creating database sessions and declarative_base for defining the base class for SQLAlchemy models
from sqlalchemy.exc import SQLAlchemyError # Importing SQLAlchemyError for handling database-related exceptions

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

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base = declarative_base()

    logger.info("Database engine initialized successfully")

except Exception as e:
    logger.exception("Failed to initialize database")
    raise


# startup connection test
def test_database_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")

    except Exception as e:
        logger.exception("Database connection failed")
        raise


def get_db():  # This function is a generator that provides a database session for use in API endpoints. It ensures that the session is properly closed after use, and includes error handling for database-related issues.
    db = SessionLocal()

    try:
        yield db

    except SQLAlchemyError:
        logger.exception("Database session error")
        db.rollback()
        raise

    except Exception:
        logger.exception("Unexpected database error")
        db.rollback()
        raise

    finally:
        db.close()