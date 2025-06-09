from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Annotated
from pydantic import Field

class Post(BaseModel): #used to define and validate schema.
    title: str
    content: str
    published: bool = True #default True if user doesnt provide => not compulsary field
    #rating: Optional[int] = None    #gives None(null) if not provided, not compulsary field

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #default True if user doesnt provide => not compulsary field

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class PostResponse(PostBase):
    id:int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]