from pydantic import BaseModel, Field


class VoteCreate(BaseModel):
    post_id: int
    # user_id: int
    direction: int = Field(le=1, ge=0)
