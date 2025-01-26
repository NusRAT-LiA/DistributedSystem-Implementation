import asyncio
from fastapi import FastAPI
from routes import post
from database import engine, Base
# from jobs import periodicCleanNotifications
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

# async def lifespan(app: FastAPI):
#     task = asyncio.create_task(periodicCleanNotifications())  
#     try:
#         yield
#     finally:
#         task.cancel()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Post Service!"}

app.include_router(post.router, prefix="/post", tags=["Post"])
