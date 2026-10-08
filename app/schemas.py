from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr

class PostBase(BaseModel):       # helps you create a schema accroding to which input happen
    title: str
    content: str 
    published:  bool =True # so if this is not providied then it defaults to true 

class PostCreate(PostBase):
    pass

class Post(PostBase):       # response model
    id:int
    created_at:datetime
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