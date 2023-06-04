from pydantic import BaseModel, EmailStr, conint, validator
from datetime import datetime
from typing import Optional


#Response for Post
class Post_Base(BaseModel):
    id: int
    song: str
    artist: str
    genre: str
    opinion: Optional[str] = None 
    spotify: Optional[str]=""
    created_at: datetime
    user_id: Optional[int] = None

    class Config:
        orm_mode = True


class Create_Post(BaseModel):
    song: str
    artist: str
    genre: str
    opinion: Optional[str] = None 
    spotify: Optional[str] = ""
    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    id: int
    song: str
    artist: str
    genre: str
    created_at: datetime
    user_id: int
    class Config:
        orm_mode = True

class UpdateOpinion(BaseModel):
    opinion: str
    
    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    direction: conint(ge=0)

    @validator('direction')
    def validate_direction(cls, value):
        if value < 0:
            raise ValueError('Direction value cannot be negative')
        return value

class ReturnedOpinion(BaseModel):
    id: int
    song: str
    artist: str
    genre: str
    opinion: str
    spotify: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True   


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class PostUserCreate(UserCreate):
    created_at: datetime 


class ReturnedUser(BaseModel):
    created_at: datetime 
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token (BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

    
