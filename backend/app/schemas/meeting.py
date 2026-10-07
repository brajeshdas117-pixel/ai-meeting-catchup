from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class MeetingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    meeting_date: datetime
    transcript: Optional[str]

class MeetingUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    meeting_date: datetime
    transcript: Optional[str] = None

class MeetingResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    meeting_date: datetime
    transcript: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

