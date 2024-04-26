from pydantic import BaseModel

from app.schemas.base import BaseCommon
from app.schemas.user import UserCreateResponse


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostCreateResponse(BaseCommon, PostBase):
    owner_id: int
    owner: UserCreateResponse


class PostVoteGetResponse(BaseModel):
    post: PostCreateResponse
    num_likes: int

    class Config:
        from_attributes = True
