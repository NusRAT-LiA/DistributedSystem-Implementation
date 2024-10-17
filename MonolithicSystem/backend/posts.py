from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import authenticate, getCurrentUser, signup
from database import getDb
from models import Post, Notification, User
from minioConfig import upload_file_to_minio
from schemas import PostCreate
from typing import List, Optional

post_router = APIRouter()

@post_router.post("/signup/")
def create_user(email: str, password: str, db: Session = Depends(getDb)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return signup(db, email, password)

@post_router.post("/signin/")
def sign_in(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getDb)):
    user = authenticate(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": user.email, "token_type": "bearer"}

# @post_router.get("/posts/", response_model=List[Post])
# def get_posts(db: Session = Depends(getDb), currentUser = Depends(getCurrentUser)):
#     return db.query(Post).filter(Post.userId != currentUser.id).order_by(Post.createdAt.desc()).all()

@post_router.post("/post/")
async def create_post(title: str, content: str, file: Optional[UploadFile] = None, db: Session = Depends(getDb), currentUser = Depends(getCurrentUser)):
    image_url = None
    if file:
        image_url = upload_file_to_minio(file)
    
    new_post = Post(title=title, content=content, image_url=image_url, userId=currentUser.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @post_router.get("/notifications/", response_model=List[Notification])
# def get_notifications(db: Session = Depends(getDb), currentUser = Depends(getCurrentUser)):
#     return db.query(Notification).filter(Notification.userId == currentUser.id).order_by(Notification.createdAt.desc()).all()

@post_router.post("/notifications/")
def create_notification(post_id: int, db: Session = Depends(getDb), currentUser = Depends(getCurrentUser)):
    new_notification = Notification(postId=post_id, userId=currentUser.id)
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification
