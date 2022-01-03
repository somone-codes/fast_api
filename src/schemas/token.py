from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    id: Optional[int] = None
