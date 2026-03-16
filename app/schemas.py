from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ItemStatusEnum(str, Enum):
    LOST = "lost"
    FOUND = "found"


class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1024)
    location: str = Field(..., min_length=1, max_length=255)
    contact: str = Field(..., min_length=3, max_length=255)
    status: ItemStatusEnum = Field(..., description="Either 'lost' or 'found'.")


class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass


class ItemUpdate(BaseModel):
    """
    Schema for updating an existing item.

    All fields are optional to allow partial updates via PUT.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1024)
    location: Optional[str] = Field(default=None, min_length=1, max_length=255)
    contact: Optional[str] = Field(default=None, min_length=3, max_length=255)
    status: Optional[ItemStatusEnum] = None


class ItemInDBBase(ItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Enables ORM mode (SQLAlchemy -> Pydantic)


class ItemResponse(ItemInDBBase):
    """Schema returned in API responses for a single item."""
    pass


class ItemsListResponse(BaseModel):
    """Schema returned when listing items."""
    items: list[ItemResponse]
    total: int