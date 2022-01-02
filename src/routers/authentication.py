from database.alchemy_orm import get_db
from schemas.user import UserLogin
from models.user import User as userModel
from utils.encrypt import validate

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):

    user = db.query(userModel).filter(user_login.email == userModel.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not validate(user.password, user_login.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    return {"token": "shhh! Secret token."}
