from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database import Base

class Meeting(Base):
    __tablename__= "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    meeting_date = Column(DateTime, nullable=False)
    transcript = Column(Text, nullable = True)
    created_at = Column(DateTime, default = datetime.utcnow)