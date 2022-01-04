from database.alchemy_orm import get_db
from schemas import post as post_schema
from models import post as post_model, user as user_model
from .authentication import validate_current_user

from typing import List, Optional

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[post_schema.Post])
def get_posts(db: Session = Depends(get_db), user: user_model = Depends(validate_current_user)):
    posts = db.query(post_model.Post).filter(post_model.Post.owner_id == user.id).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post_schema.Post)
def create_posts(post: post_schema.PostCreate, db: Session = Depends(get_db),
                 user: user_model = Depends(validate_current_user)):
    new_post = post_model.Post(owner_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=post_schema.Post)
def get_post(id: int, db: Session = Depends(get_db), user: user_model = Depends(validate_current_user)):
    post_query = db.query(post_model.Post).filter(post_model.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform this action.")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: user_model = Depends(validate_current_user)):
    post_query = db.query(post_model.Post).filter(post_model.Post.id == id)

    post: Optional[post_model] = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform this action.")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=post_schema.Post)
def update_post(id: int, updated_post: post_schema.PostCreate, db: Session = Depends(get_db),
                user: user_model = Depends(validate_current_user)):
    post_query = db.query(post_model.Post).filter(post_model.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform this action.")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
