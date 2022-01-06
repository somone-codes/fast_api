from .authentication import validate_current_user
from database.alchemy_orm import get_db
from models.user import User as User_Model
from schemas.vote import Vote as Vote_Schema
from models.post import Post as Post_Model
from models.vote import Vote as Vote_Model

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/")
def add_remove_vote(vote: Vote_Schema, db: Session = Depends(get_db), user: User_Model = Depends(validate_current_user)):

    if not db.query(Post_Model).filter(vote.post_id == Post_Model.id).first():
        # post trying to vote on doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post found with id {vote.post_id}")

    vote_query = db.query(Vote_Model).filter(vote.post_id == Vote_Model.post_id).filter(user.id == Vote_Model.user_id)

    if vote_query.first():
        if vote.vote:
            #  vote already exists and still trying to vote on same post then fail
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Already voted on the post with id {vote.post_id}")
        #  vote already exists and requesting to remove
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote has been deleted."}
    else:
        # vote doesn't exist but asking to remove vote
        if not vote.vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist.")
        # new Vote
        new_vote = Vote_Model(post_id=vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote has been added."}



