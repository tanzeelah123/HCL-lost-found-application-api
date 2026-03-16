from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

DbSessionDep = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=schemas.ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a lost or found item",
)
def create_item(
    item_in: schemas.ItemCreate,
    db: DbSessionDep,
) -> schemas.ItemResponse:
    """
    Create a new lost or found item record.
    """
    db_item = crud.create_item(db=db, item_in=item_in)
    return schemas.ItemResponse.model_validate(db_item)


@router.get(
    "",
    response_model=schemas.ItemsListResponse,
    summary="Retrieve all items",
)
def list_items(
    db: DbSessionDep,
    skip: int = Query(0, ge=0, description="Number of items to skip."),
    limit: int = Query(
        50,
        ge=1,
        le=1000,
        description="Maximum number of items to return.",
    ),
) -> schemas.ItemsListResponse:
    """
    Retrieve a paginated list of lost and found items.
    """
    items = crud.get_items(db=db, skip=skip, limit=limit)
    total = crud.count_items(db=db)
    return schemas.ItemsListResponse(
        items=[schemas.ItemResponse.model_validate(item) for item in items],
        total=total,
    )


@router.get(
    "/{item_id}",
    response_model=schemas.ItemResponse,
    summary="Retrieve a single item by ID",
)
def get_item(
    item_id: int,
    db: DbSessionDep,
) -> schemas.ItemResponse:
    """
    Retrieve a specific item by its unique identifier.
    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found.",
        )
    return schemas.ItemResponse.model_validate(db_item)


@router.put(
    "/{item_id}",
    response_model=schemas.ItemResponse,
    summary="Update an item",
)
def update_item(
    item_id: int,
    item_in: schemas.ItemUpdate,
    db: DbSessionDep,
) -> schemas.ItemResponse:
    """
    Update details of an existing item.

    All fields are optional; only the provided fields will be updated.
    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found.",
        )

    updated_item = crud.update_item(db=db, db_item=db_item, item_in=item_in)
    return schemas.ItemResponse.model_validate(updated_item)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
)
def delete_item(
    item_id: int,
    db: DbSessionDep,
) -> None:
    """
    Delete an item by its unique identifier.
    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found.",
        )

    crud.delete_item(db=db, db_item=db_item)