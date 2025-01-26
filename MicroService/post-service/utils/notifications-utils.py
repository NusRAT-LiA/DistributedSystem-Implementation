import requests
from typing import Optional
from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException, status, Header
from sqlalchemy.orm import Session
from models import Post
from schemas import PostCreate, PostOut
from database import getDb
from utils.minio_utils import uploadCodeSnippet, getCodeSnippet
from utils.auth_utils import getCurrentUser

router = APIRouter()

# URL for the notification service
NOTIFICATION_SERVICE_URL = "http://localhost:8002/notification/"


def createPost(
    content: str = Form(...),
    codeFile: Optional[UploadFile] = File(None),
    db: Session = Depends(getDb),
    authorization: str = Header(...)
):
    token = authorization.split(" ")[1]
    currentUser = getCurrentUser(token)  # Fetch user from the auth service

    # Create post
    dbPost = Post(content=content, userId=currentUser.id)
    db.add(dbPost)
    db.commit()
    db.refresh(dbPost)
    
    # Upload code file if provided
    if codeFile:
        fileName = f"{dbPost.id}_{codeFile.filename}"
        uploadCodeSnippet(codeFile.file, fileName)

    # Prepare the notification message
    notificationMessage = f"New post created by {currentUser.email}: {dbPost.content[:30]}..."

    # Send notification by calling the notification service API
    notification_payload = {
        "postId": dbPost.id,
        "message": notificationMessage
    }

    try:
        response = requests.post(NOTIFICATION_SERVICE_URL, json=notification_payload)
        response.raise_for_status()  # Raise an error for bad responses (4xx/5xx)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to create notification: {str(e)}")

    return dbPost
