from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models import User
from typing import Optional
from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    createdAt: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    description: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    ownerId: int
    owner: User
    createdAt: datetime

    class Config:
        from_attributes = True


class PostOut(PostBase):
    post: Post
    votes: int


class Token(BaseModel):
    accessToken: str
    tokenType: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    postId: int
    dir: conint(ge=0, le=1)
