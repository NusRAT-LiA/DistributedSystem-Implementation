from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashedPassword = Column(String, nullable=False)

    posts = relationship("Post", back_populates="user")
    notifications = relationship("NotificationStatus", back_populates="user")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    userId = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="posts")

    notifications = relationship("Notification", back_populates="post")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    postId = Column(Integer, ForeignKey("posts.id"))
    message = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.now(timezone.utc))
    post = relationship("Post", back_populates="notifications")

    seenStatus = relationship("NotificationStatus", back_populates="notification")

class NotificationStatus(Base):
   __tablename__ = "notification_status"
   id = Column(Integer, primary_key=True, index=True)
   notificationId = Column(Integer, ForeignKey("notifications.id"))
   userId = Column(Integer, ForeignKey("users.id"))
   seen = Column(Boolean, default=False)

   notification = relationship("Notification", back_populates="seenStatus")
   user = relationship("User", back_populates="notifications")