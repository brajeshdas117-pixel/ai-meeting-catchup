
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.meeting import Meeting
from app.models.recording import MeetingRecording

router = APIRouter(
    prefix="/meetings",
    tags=["Meeting Audio"],
)

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".webm"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


@router.post("/{meeting_id}/upload-audio")
def upload_meeting_audio(
    meeting_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id
    ).first()

    if meeting is None:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found",
        )

    original_name = Path(file.filename or "").name
    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio extension",
        )

    saved_name = f"{uuid4().hex}{extension}"
    destination = UPLOAD_DIR / saved_name
    total_size = 0

    try:
        with destination.open("wb") as output:
            while chunk := file.file.read(1024 * 1024):
                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Audio file exceeds the 100 MB limit",
                    )

                output.write(chunk)

        recording = MeetingRecording(
            meeting_id=meeting_id,
            original_filename=original_name,
            stored_filename=saved_name,
            file_path=str(destination),
            content_type=file.content_type,
            size_bytes=total_size,
        )

        db.add(recording)
        db.commit()
        db.refresh(recording)

        return {
            "message": "Audio uploaded and metadata saved successfully",
            "recording_id": recording.id,
            "meeting_id": recording.meeting_id,
            "original_filename": recording.original_filename,
            "saved_filename": recording.stored_filename,
            "content_type": recording.content_type,
            "size_bytes": recording.size_bytes,
            "uploaded_at": recording.uploaded_at,
        }

    except Exception:
        db.rollback()
        destination.unlink(missing_ok=True)
        raise

    finally:
        file.file.close()
