from fastapi import FastAPI
from routes import auth, post, notification
from database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}
# Include routers for the endpoints
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(post.router, prefix="/post", tags=["Post"])
app.include_router(notification.router, prefix="/notification", tags=["Notification"])
