from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import models
import schemas
from routers.auth_users import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):    
    return db.query(models.Item).filter(models.Item.owner_id == user_id).offset(skip).limit(limit).all()


def update_item(db: Session, item_id: int, item_update: schemas.ItemCreate):    
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise NoResultFound(f"Item with id {item_id} does not exist")
    
    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise NoResultFound(f"Item with id {item_id} does not exist")

    db.delete(item)
    db.commit()
    return {"msg": f"Item with id {item_id} was deleted"}
