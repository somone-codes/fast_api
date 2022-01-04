from database.alchemy_orm import get_db
from models.user import User as userModel
from utils.encrypt import validate
from utils.oauth2 import create_token, validate_token
from schemas.token import Token, TokenData as Token_Data_Schema

from os import getenv

from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])

TOKEN_URL = getenv("TOKEN_URL")

oauth2_schema = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


@router.post("/login", response_model=Token)
def login(user_login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(userModel).filter(user_login.username == userModel.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not validate(user.password, user_login.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    token = create_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}


def validate_current_user(token: str = Depends(oauth2_schema),  db: Session = Depends(get_db)) -> int:
    auth_failure_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Credential validation failed.",
                                           headers={"WWW-Authenticate": "bearer"})

    token = validate_token(token, ["user_id"], schema=Token_Data_Schema, invalid_creds_error=auth_failure_exception)

    user = db.query(userModel).filter(userModel.id == token.user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials, user not found.")

    return user

