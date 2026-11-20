
from fastapi import FastAPI

from app.routers import jobs, profiles


# Create the FastAPI application
app = FastAPI(
    title="AI Job Search Agent",
    description="An AI-powered assistant for finding and evaluating job opportunities.",
    version="0.1.0"
)


# Register API routers
app.include_router(jobs.router)
app.include_router(profiles.router)


# First endpoint: Welcome message
@app.get("/")
def home():
    return {
        "message": "Welcome to AI Job Search Agent!",
        "status": "running"
    }


# Second endpoint: Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI Job Search Agent"
    }
