from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import getDb
from models import User
from schemas import TokenData
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

def createAccessToken(data: dict):
    toEncode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    toEncode.update({"exp": expire})
    encoded_jwt = jwt.encode(toEncode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(getDb)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        tokenData = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == tokenData.email).first()
    if user is None:
        raise credentials_exception
    return user
