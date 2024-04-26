from sqlalchemy.orm import Session

from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.models.user import User
from app.database import get_db
from app.schemas.user import UserCreate, UserCreateResponse
from app.utils import hash_password


router = APIRouter(tags=["Users"], prefix="/users")


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse
)
async def create_users(
    user: Annotated[UserCreate, Body(...)], db: Annotated[Session, Depends(get_db)]
):

    # hash the password -> user.password

    user.password = hash_password(user.password)
    new_user = User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=UserCreateResponse)
async def get_user(id: int, db: Annotated[Session, Depends(get_db)]):

    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={id} not found.",
        )

    return user
