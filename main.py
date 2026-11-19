
from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(
    title="AI Job Search Agent",
    description="An AI-powered assistant for finding and evaluating job opportunities.",
    version="0.1.0"
)


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
