from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class NotificationBase(BaseModel):
    message: str

class NotificationCreate(NotificationBase):
    postId: int

class NotificationOut(NotificationBase):
    id: int
    postId: int
    createdAt: datetime
    seen: bool = False


