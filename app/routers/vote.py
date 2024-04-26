from sqlalchemy.orm import Session

from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status


from app.database import get_db
from app.models.user import User
from app.models.post import Post
from app.models.vote import Vote
from app.oauth2 import get_current_user
from app.schemas.vote import VoteCreate


router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote: Annotated[VoteCreate, Body()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_current_user)],
):
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={vote.post_id} not found.",
        )
    vote_query = db.query(Vote).filter(
        Vote.post_id == vote.post_id, Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.direction == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User{current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return Response(content="Successfully added vote.")
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return Response(content="Successfully deleted vote.")
