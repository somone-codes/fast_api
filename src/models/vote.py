from database.alchemy_orm import Base

from sqlalchemy import Column, ForeignKey, Integer


class Vote(Base):
    __tablename__ = "votes"
    
    post_id: int = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id: int = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
