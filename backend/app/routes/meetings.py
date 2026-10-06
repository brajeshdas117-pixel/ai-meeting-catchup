from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingCreate

router = APIRouter(
    prefix="/meetings",
    tags=["Meetings"]
)


@router.post("/")
def create_meeting(
    meeting: MeetingCreate,
    db: Session = Depends(get_db)
):
    new_meeting = Meeting(
        title=meeting.title,
        date=meeting.date,
        duration=meeting.duration,
        summary=meeting.summary
    )

    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    return new_meeting

@router.get("/")
def get_meetings(db: Session = Depends(get_db)):
    meetings = db.query(Meeting).all()
    return meetings