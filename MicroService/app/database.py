from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# postgresql://<username>:<password>@<host>:<port>/<database_name>
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.pgUsername}:{settings.pgPassword}@{settings.pgHost}:{settings.pgPort}/{settings.pgDatabase}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
