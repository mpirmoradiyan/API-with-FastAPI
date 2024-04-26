from pydantic import BaseModel, EmailStr

from app.schemas.base import BaseCommon


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserCreateResponse(BaseCommon):
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None
