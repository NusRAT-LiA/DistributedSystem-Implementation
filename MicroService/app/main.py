import asyncio
from fastapi import FastAPI
from routes import auth, post, notification
from database import engine, Base
from jobs import periodicCleanNotifications
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

# app = FastAPI()
async def lifespan(app: FastAPI):
    task = asyncio.create_task(periodicCleanNotifications())  
    try:
        yield
    finally:
        task.cancel()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(post.router, prefix="/post", tags=["Post"])
app.include_router(notification.router, prefix="/notification", tags=["Notification"])
