import asyncio
from sqlalchemy.orm import Session
from models import Notification
from datetime import datetime, timedelta, timezone
from database import getDb

async def periodicCleanNotifications():
    while True:
        cleanOldNotifications()  
        await asyncio.sleep(3600)
        
def cleanOldNotifications():
    db: Session = next(getDb())
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    db.query(Notification).filter(Notification.createdAt < cutoff).delete()
    db.commit()
    db.close()
