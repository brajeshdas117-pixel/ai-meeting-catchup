from fastapi import FastAPI
from app.routes.health import router as health_router

from app.database import Base, engine
from app.models.meeting import Meeting
from app.routes.meetings import router as meetings_router
from app.routes import meetings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Meeting Catch-Up Assistant",
    description="Backend API for processing meeting recordings and generating AI-powered meeting summaries.",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(meetings_router)
app.include_router(meetings.router)

@app.get("/")
def root():
    return {
        "message": "AI Meeting Catch-Up Assistant API is running!"
    }