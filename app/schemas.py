from datetime import datetime
from pydantic import BaseModel, ConfigDict


# Fields required when creating a job
class JobCreate(BaseModel):
    title: str
    company: str
    location: str | None = None
    description: str | None = None
    requirements: str | None = None
    application_url: str | None = None
    source: str | None = None


# Fields returned when reading a job
class JobResponse(JobCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)