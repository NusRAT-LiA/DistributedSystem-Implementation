from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from utils.auth_utils import getCurrentUser
from models import Notification, NotificationStatus, User
from schemas import NotificationCreate, NotificationOut
from database import getDb

router = APIRouter()

@router.post("/", response_model=NotificationOut)
def createNotification(
    # postId: int,
    # message: str,
    notification_create: NotificationCreate, 
    db: Session = Depends(getDb)  
):
    postId = notification_create.postId
    message = notification_create.message
    dbNotification = Notification(
        postId=postId,
        message=message
    )
    db.add(dbNotification)
    db.commit()
    db.refresh(dbNotification)

    return NotificationOut(
        id=dbNotification.id,
        postId=dbNotification.postId,
        message=dbNotification.message,
        createdAt=datetime.now(timezone.utc)  
    )

@router.put("/{notification_id}/mark_seen")
def markNotificationSeen(
    notification_id: int,
    db: Session = Depends(getDb),
    authorization: str = Header(...)
):
    token = authorization.split(" ")[1]
    currentUser = getCurrentUser(token)
    status = db.query(NotificationStatus).filter(
        NotificationStatus.notificationId == notification_id,
        NotificationStatus.userId == currentUser.id
    ).first()

    if status:
        status.seen = True
    else:
        status = NotificationStatus(userId=currentUser.id, notificationId=notification_id, seen=True)
        db.add(status)

    db.commit()
    return {"message": "Notification marked as seen"}

@router.get("/", response_model=list[NotificationOut])
def getNotifications(
    db: Session = Depends(getDb),
    authorization: str = Header(...)
):
    token = authorization.split(" ")[1]
    currentUser = getCurrentUser(token)

    notifications = db.query(Notification).all()
    statuses = db.query(NotificationStatus).filter(NotificationStatus.userId == currentUser.id).all()
    status_map = {status.notificationId: status.seen for status in statuses}

    return [
        NotificationOut(
            id=notif.id,
            postId=notif.postId,
            message=notif.message,
            createdAt=notif.createdAt,
            seen=status_map.get(notif.id, False)
        )
        for notif in notifications
    ]