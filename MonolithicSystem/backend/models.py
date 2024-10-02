from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    image_url = Column(String, nullable=True)
    userId = Column(Integer, ForeignKey('users.id'))
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    postId = Column(Integer, ForeignKey('posts.id'))
    userId = Column(Integer, ForeignKey('users.id'))
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
