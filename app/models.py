from __future__ import annotations

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, Integer, String

from .database import Base


class ItemStatus(str, PyEnum):
    LOST = "lost"
    FOUND = "found"


class Item(Base):
    """
    SQLAlchemy ORM model representing a lost or found item in the system.
    """

    __tablename__ = "items"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(255), nullable=False, index=True)
    description: str = Column(String(1024), nullable=True)
    location: str = Column(String(255), nullable=False)
    contact: str = Column(String(255), nullable=False)
    status: ItemStatus = Column(
        Enum(ItemStatus, name="item_status"), nullable=False, index=True
    )
    created_at: datetime = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )