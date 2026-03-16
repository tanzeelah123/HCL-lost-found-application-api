from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def create_item(db: Session, item_in: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(
        title=item_in.title,
        description=item_in.description,
        location=item_in.location,
        contact=item_in.contact,
        status=models.ItemStatus(item_in.status.value),
    )
    db.add(db_item)
    db.flush()  # populate primary key
    return db_item


def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    stmt = select(models.Item).where(models.Item.id == item_id)
    return db.scalar(stmt)


def get_items(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> List[models.Item]:
    stmt = (
        select(models.Item)
        .order_by(models.Item.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(stmt))


def count_items(db: Session) -> int:
    return db.query(models.Item).count()


def update_item(
    db: Session,
    db_item: models.Item,
    item_in: schemas.ItemUpdate,
) -> models.Item:
    data = item_in.model_dump(exclude_unset=True)

    if "status" in data and data["status"] is not None:
        # Convert Pydantic enum to SQLAlchemy enum
        data["status"] = models.ItemStatus(data["status"].value)

    for field, value in data.items():
        setattr(db_item, field, value)

    db.add(db_item)
    db.flush()
    return db_item


def delete_item(db: Session, db_item: models.Item) -> None:
    db.delete(db_item)
    db.flush()