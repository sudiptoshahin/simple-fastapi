from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str
    
# -------------
# BASE MODEL
# ------------

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id: str
    created_at: datetime
    owner_id: str
    owner: UserResponse

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]=None


class APIResponse(BaseModel):
    code: int
    status: str
    message: str


class Vote(BaseModel):
    post_id: str
    dir: conint(le=1) # type: ignore