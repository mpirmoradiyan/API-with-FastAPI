from sqlalchemy import func
from sqlalchemy.orm import Session

from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Response, status

from app.models.post import Post
from app.models.vote import Vote
from app.database import get_db
from app.models.user import User
from app.oauth2 import get_current_user
from app.schemas.post import PostCreate, PostCreateResponse, PostVoteGetResponse


router = APIRouter(tags=["Posts"], prefix="/posts")


@router.get("/", response_model=list[PostVoteGetResponse])
# @router.get("/", response_model=list[PostCreateResponse])
# @router.get("/")
async def get_posts(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_current_user)],
    limit: Annotated[int, Query()] = 10,
    skip: Annotated[int, Query()] = 0,
    search: Annotated[str, Query()] = "",
):
    # cursor.execute("SELECT * FROM posts;")
    # data = cursor.fetchall()
    #

    # print(posts_data)

    posts_data = (
        db.query(Post, func.count(Vote.post_id).label("num_likes"))
        .join(Vote, onclause=Post.id == Vote.post_id, isouter=True)
        .group_by(Post.id)
        .filter(Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    # print(posts_data)

    posts_data = [
        {"post": post, "num_likes": num_likes} for post, num_likes in posts_data
    ]

    return posts_data

    # return posts_votes_join_res


@router.get("/{id}", response_model=PostVoteGetResponse)
async def get_post(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_current_user)],
):
    # cursor.execute("SELECT * FROM posts WHERE id=%s", (str(id)))
    # post = cursor.fetchall()

    # post = db.query(Post).filter(Post.id == id).first()

    post = (
        db.query(Post, func.count(Vote.post_id).label("num_likes"))
        .join(Vote, onclause=Post.id == Vote.post_id, isouter=True)
        .group_by(Post.id)
        .filter(Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={id} not found.",
        )

    # if post.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to perform the requested action",
    #     )
    post = {"post": post[0], "num_likes": post[1]}

    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=PostCreateResponse
)
async def create_posts(
    post: Annotated[PostCreate, Body(...)],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_current_user)],
):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_current_user)],
):
    # cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *;", (str(id),))
    # deleted = cursor.fetchall()
    # conn.commit()

    post = db.query(Post).filter(Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={id} not found.",
        )

    if post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform the requested action",
        )

    post.delete(synchronize_session=False)

    db.commit()

    return Response(
        status_code=status.HTTP_200_OK,
        content=f"Successfully deleted the post with id={id}",
    )


@router.put("/{id}", response_model=PostCreateResponse)
async def update_post(
    id: int,
    post: Annotated[PostCreate, Body(...)],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_current_user)],
):

    # cursor.execute(
    #     "UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchall()
    # conn.commit()

    query_post = db.query(Post).filter(Post.id == id)

    if not query_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={id} not found.",
        )

    if query_post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform the requested action",
        )

    query_post.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return query_post.first()
