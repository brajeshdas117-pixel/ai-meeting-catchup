from datetime import datetime
from pydantic import BaseModel

class MeetingCreate(BaseModel):
    title: str
    date: datetime
    duration: int | None = None
    summary: str | None =  None