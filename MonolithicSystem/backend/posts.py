from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from auth import getCurrentUser
from database import getDb
from models import Post, Notification
from minioConfig import upload_file_to_minio
from schemas import PostCreate
from typing import Optional

post_router = APIRouter()

@post_router.post("/post/")
async def createPost(title: str, content: str, file: Optional[UploadFile] = None, db: Session = Depends(getDb), currentUser = Depends(getCurrentUser)):
    image_url = None

    if file:
        image_url = upload_file_to_minio(file)

    newPost = Post(title=title, content=content, image_url=image_url, userId=currentUser.id)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost
