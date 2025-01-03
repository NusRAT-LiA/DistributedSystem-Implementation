from sqlalchemy import text
from database import SessionLocal, engine, Base
from sqlalchemy.exc import OperationalError

def test_db_connection():
    Base.metadata.create_all(bind=engine)
    
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("Database connection successful.")
    except OperationalError as e:
        print("Database connection failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_db_connection()
