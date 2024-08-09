from typing import Annotated, List
from fastapi import APIRouter, Body, Depends, HTTPException
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

@router.get("", response_model=List[schemas.Item])
def get_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=1)


@router.put("/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, updated_item: Annotated[schemas.ItemCreate, Body(embed=True)], db: Session = Depends(get_db)):
    item = crud.update_item(db=db, item_id=item_id, item_update=updated_item)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", response_model=dict)
def delete_items(item_id: int, db: Session = Depends(get_db)):
    result = crud.delete_item(db=db, item_id=item_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Deleted item with id {item_id}"}
