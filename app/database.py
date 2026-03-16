from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE_URL = "sqlite:///./lost_found.db"


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""


# `check_same_thread=False` is required for SQLite when used with FastAPI/Uvicorn
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    The session is committed and closed automatically after the request
    lifecycle completes, or rolled back if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()