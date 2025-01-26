from fastapi import FastAPI
from routes import auth
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Auth Service!"}

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
