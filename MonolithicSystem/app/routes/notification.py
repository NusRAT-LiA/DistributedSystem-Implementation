from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Notification
from schemas import NotificationCreate, NotificationOut
from database import getDb

router = APIRouter()

@router.post("/", response_model=NotificationOut)
def createNotification(
    postId: int,
    message: str,
    db: Session = Depends(getDb),
    
):
    dbNotification = Notification(
        postId=postId,
        message=message
    )
    db.add(dbNotification)
    db.commit()
    db.refresh(dbNotification)

    return dbNotification

@router.get("/", response_model=list[NotificationOut])
def getNotifications(db: Session = Depends(getDb)):
    notifications = db.query(Notification).all()
    return notifications
