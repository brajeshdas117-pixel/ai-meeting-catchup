from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

class Meeting(Base):
    __tablename__= "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)
    summary = Column(Text, nullable=True)