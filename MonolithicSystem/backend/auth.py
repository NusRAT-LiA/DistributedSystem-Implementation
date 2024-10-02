from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import getDb
from models import User
from fastapi.security import OAuth2PasswordBearer

cryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauthScheme = OAuth2PasswordBearer(tokenUrl="token")

def verifyPassword(plain_password, hashed_password):
    return cryptContext.verify(plain_password, hashed_password)

def getPasswordHash(password):
    return cryptContext.hash(password)

def authenticate(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verifyPassword(password, user.hashed_password):
        return False
    return user

def getCurrentUser(db: Session = Depends(getDb), token: str = Depends(oauthScheme)):
    user = db.query(User).filter(User.email == token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user
