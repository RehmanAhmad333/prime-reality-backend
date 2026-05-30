# prime-reality-backend/core/database.py

import os
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

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


def get_db():
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