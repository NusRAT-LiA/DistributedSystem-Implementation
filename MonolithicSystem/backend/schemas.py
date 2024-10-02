from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str
    image_url: str = None

class NotificationCreate(BaseModel):
    post_id: int
    user_id: int
