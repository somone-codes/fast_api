from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: Optional[datetime]
    published: Optional[bool] = True

    class Config:
        orm_mode = True


class PostOut(PostBase):

    class Config:
        orm_mode = True
