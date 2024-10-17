# from fastapi import FastAPI, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from auth import getCurrentUser
# from database import getDb
# from posts import post_router
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(post_router)

# @app.get("/")
# def root():
#     return {"message": "Welcome to the StackOverflow clone!"}
from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from auth import getCurrentUser
from database import getDb, create_database
from posts import post_router
from fastapi.middleware.cors import CORSMiddleware
from models import Notification
from datetime import datetime, timedelta

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
    create_database()

    return {"message": "Welcome to the StackOverflow clone!"}

# async def lifespan(app: FastAPI):
#     # Create database tables on startup
#     print("Creating database...")

#     create_database()
#     yield  # This marks the end of the startup phase
#     # Add any shutdown logic here if needed (like closing connections)

# app.lifespan = lifespan  # Assign the lifespan function to the app

def clean_old_notifications(db: Session):
    # Define your criteria for cleaning old notifications
    expiration_time =  datetime.now(datetime.timezone.utc) - timedelta(days=30)  # Example: Delete notifications older than 30 days
    db.query(Notification).filter(Notification.createdAt < expiration_time).delete()
    db.commit()

@app.post("/notifications/clean/")
def clean_notifications(background_tasks: BackgroundTasks, db: Session = Depends(getDb)):
    background_tasks.add_task(clean_old_notifications, db)
    return {"message": "Notification cleaner job started."}
