# schemas.py
from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    userId: int

    