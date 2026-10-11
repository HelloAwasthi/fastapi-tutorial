from datetime import datetime
from typing import Optional,Literal
from pydantic import BaseModel,EmailStr

class PostBase(BaseModel):       # helps you create a schema accroding to which input happen
    title: str
    content: str 
    published:  bool =True # so if this is not providied then it defaults to true 

class PostCreate(PostBase):
    pass

class UserOut (BaseModel):
    email: EmailStr
    id:int
    created_at:datetime
    class Config:
        orm_mode=True

class Post(PostBase):       # response model
    id:int
    created_at:datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
            orm_mode=True
    

class UserCreate (BaseModel):
    email: EmailStr
    password: str

class UserOut (BaseModel):
    email: EmailStr
    id:int
    created_at:datetime
    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token (BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] =None

class Vote(BaseModel):
    post_id:int
    dir:Literal[0,1]