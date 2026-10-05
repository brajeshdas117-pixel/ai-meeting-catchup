from fastapi import FastAPI

from app.routes.health import router as health_router

app = FastAPI(
    title="AI Meeting Catch-Up Assistant",
    description="Backend API for processing meeting recordings and generating AI-powered meeting summaries.",
    version="1.0.0"
)

app.include_router(health_router)

@app.get("/")
def root():
    return {
        "message": "AI Meeting Catch-Up Assistant API is running!"
    }