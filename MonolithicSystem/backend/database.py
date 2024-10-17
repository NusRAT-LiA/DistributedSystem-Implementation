# database.py
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/StackOverflow"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def create_database():
    logger.info("Attempting to create database tables.")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
        
        # Check the database connection by querying the current time
        with SessionLocal() as db:
            result = db.execute("SELECT NOW()").scalar()
            logger.info(f"Database connected successfully. Current time: {result}")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
