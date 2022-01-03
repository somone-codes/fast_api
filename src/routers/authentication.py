from database.alchemy_orm import get_db
from schemas.user import UserLogin
from models.user import User as userModel
from utils.encrypt import validate
from utils.oauth2 import create_token

from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(userModel).filter(user_login.username == userModel.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not validate(user.password, user_login.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    token = create_token({"user_id": user.email})
    return {"access_token": token, "token_type": "bearer"}
