from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    userId: int
    codeFile: Optional[str] = None

    class Config:
        from_attributes = True

class NotificationBase(BaseModel):
    message: str

class NotificationCreate(NotificationBase):
    postId: int

class NotificationOut(NotificationBase):
    id: int
    postId: int
    createdAt: datetime
    seen: bool = False


