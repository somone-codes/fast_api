from database.alchemy_orm import Base

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False, index=True)
    content = Column(String, unique=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    published = Column(Boolean, nullable=False, server_default='True')
