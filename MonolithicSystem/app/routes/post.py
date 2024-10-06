from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from models import Post, User
from schemas import PostCreate, PostOut
from database import getDb
from utils.minio_utils import uploadCodeSnippet
from utils.jwt import getCurrentUser
from routes.notification import createNotification  


router = APIRouter()

@router.get("/", response_model=list[PostOut])
def getPosts(db: Session = Depends(getDb), currentUser: User = Depends(getCurrentUser)):
    posts = db.query(Post).filter(Post.userId != currentUser.id).all()
    # posts = db.query(Post).all() 
    return posts

@router.post("/", response_model=PostOut)
def createPost(
    content:str,
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
    createNotification(db, dbPost.id, notificationMessage)
    
    return dbPost
