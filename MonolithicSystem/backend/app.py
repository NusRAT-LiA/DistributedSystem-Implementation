from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import getCurrentUser
from database import getDb
from posts import post_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)

@app.get("/")
def root():
    return {"message": "Welcome to the StackOverflow clone!"}
