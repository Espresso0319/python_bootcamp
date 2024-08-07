from typing import Annotated, List

from fastapi import APIRouter, Body, Depends

from data_types import Item, User
from dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def get_items(skip: int = 0, limit: int = 10):
    return {"message": "Get all items", "skip": skip, "limit": limit}


@router.get("/{item_id}")
def get_item(item_id: int):
    return {"message": f"Get item with id {item_id}"}


@router.get("/{item_id}/subitems/{subitem_id}")
def get_subitem(item_id: int, subitem_id: int | str, q: str = None):
    return {"item_id": item_id, "subitem_id": subitem_id, "q": q}


@router.post("/")
def create_items(items: List[Item]):
    return {"message": "create items", "items": items}


@router.post("/{item_id}/subitems", tags=["async"])
async def create_subitems(item_id: int, subitems: List[Item], user: User = None, stack: Annotated[int, Body()] = 0):
    return {
        "message": f"create subitems for item with id {item_id}",
        "subitems": subitems,
        "user": user,
        "stack": stack,
    }


@router.put("/{item_id}")
def update_item(item_id: int, updated_item: Annotated[Item, Body(embed=True)] = None):
    return {"message": f"Updated item with id {item_id}", "updated": updated_item}


@router.delete("/{item_id}")
def delete_items(item_id: int):
    return {"message": f"Deleted item with id {item_id}"}
