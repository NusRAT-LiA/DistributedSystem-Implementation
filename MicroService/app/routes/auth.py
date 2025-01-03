from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import getDb
from models import User
from schemas import UserCreate, Token
from utils.hash import getPasswordHash, verifyPassword
from utils.jwt import createAccessToken
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/signup", response_model=dict)
def signup(user: UserCreate, db: Session = Depends(getDb)):
    dbUser = db.query(User).filter(User.email == user.email).first()
    if dbUser:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashedPassword = getPasswordHash(user.password)
    newUser = User(email=user.email, hashedPassword=hashedPassword)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return {"msg": "User created successfully"}

@router.post("/signin", response_model=Token)
def signin(user: UserCreate, db: Session = Depends(getDb)):
    dbUser = db.query(User).filter(User.email == user.email).first()
    if not dbUser or not verifyPassword(user.password, dbUser.hashedPassword):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    accessToken = createAccessToken(data={"sub": dbUser.email})
    return {"accessToken": accessToken, "tokenType": "bearer"}
