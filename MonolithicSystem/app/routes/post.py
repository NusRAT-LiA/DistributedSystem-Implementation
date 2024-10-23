from typing import Optional
from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from models import Post, User
from schemas import PostCreate, PostOut
from database import getDb
from utils.minio_utils import uploadCodeSnippet, getCodeSnippet
from utils.jwt import getCurrentUser
from routes.notification import createNotification  


router = APIRouter()

@router.get("/", response_model=list[PostOut])
def getPosts(db: Session = Depends(getDb)):
    posts = db.query(Post).all()  # Fetch all posts from the database

    for post in posts:
        codeSnippet = getCodeSnippet(post.id)  # Check if any file exists in MinIO for this post ID
        if codeSnippet:
            post.codeFile = codeSnippet # Assign a default filename based on post ID
        else:
            post.codeFile = None  # If no file exists, set it to None

    return posts

@router.post("/", response_model=PostOut)
def createPost(
    content: str = Form(...),
    codeFile: Optional[UploadFile] = File(None),
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentUser)
):
    dbPost = Post(content=content, userId=currentUser.id)
    db.add(dbPost)
    db.commit()
    db.refresh(dbPost)
    if codeFile:
        fileName = f"{dbPost.id}_{codeFile.filename}"
        uploadCodeSnippet(codeFile.file, fileName)

    notificationMessage = f"New post created by {currentUser.email}: {dbPost.content[:30]}..."
    createNotification(postId=dbPost.id, message=notificationMessage, db=db)
    
    return dbPost