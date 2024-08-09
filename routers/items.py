from typing import Annotated, List
from fastapi import APIRouter, Body, Depends
from data_types import Item, User


from sqlalchemy.orm import Session
import crud
import schemas
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/items",
    tags=["Blogs"],    
    responses={404: {"description": "Not found"}},
)

@router.get("")
def get_items(skip: int = 0, limit: int = 10):
    return {"message": "Get all items", "skip": skip, "limit": limit}


@router.get("/{item_id}")
def get_item(item_id: int):
    return {"message": f"Get item with id {item_id}"}


@router.post("/")
def create_blog(item: schemas.ItemBase, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id='1')


@router.put("/{item_id}")
def update_item(item_id: int, updated_item: Annotated[Item, Body(embed=True)] = None):
    return {"message": f"Updated item with id {item_id}", "updated": updated_item}


@router.delete("/{item_id}")
def delete_items(item_id: int):
    return {"message": f"Deleted item with id {item_id}"}
