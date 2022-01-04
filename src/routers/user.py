from routers.authentication import validate_current_user
from schemas import user as user_schema
from models import user as user_model
from database.alchemy_orm import get_db
from utils.encrypt import encrypt

from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[user_schema.UserOut])
def get_users(db: Session = Depends(get_db), user: user_model = Depends(validate_current_user)):
    users = db.query(user_model.User).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No users exist.")

    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserOut)
def create_users(user: user_schema.UserCreate, db: Session = Depends(get_db),
                 logged_user: user_model = Depends(validate_current_user)):
    user.password = encrypt(user.password)

    new_user = user_model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=user_schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db), user: user_model = Depends(validate_current_user)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user


@router.delete('/{id}')
def get_user(id: int, db: Session = Depends(get_db), logged_user: user_model = Depends(validate_current_user)):
    user_query = db.query(user_model.User).filter(user_model.User.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    if user.id != logged_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not authorised to perform this action.")
    user_query.delete(synchronize_session=False)
    db.commit()
