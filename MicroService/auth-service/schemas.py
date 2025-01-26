from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    accessToken: str
    tokenType: str

class TokenData(BaseModel):
    email: str = None