from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    postId = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.now(timezone.utc))


class NotificationStatus(Base):
   __tablename__ = "notification_status"
   id = Column(Integer, primary_key=True, index=True)
   notificationId = Column(Integer, ForeignKey("notifications.id"))
   userId = Column(Integer, nullable=False)
   seen = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)  # Add email if necessary
