
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import JobResponse
from app.services.profile_job_search_service import (
    search_jobs_for_profile
)


router = APIRouter(
    prefix="/profile-search",
    tags=["Profile-Based Job Search"]
)


@router.get("/{profile_id}", response_model=list[JobResponse])
def search_profile_jobs(
    profile_id: int,
    db: Session = Depends(get_db)
):
    jobs = search_jobs_for_profile(db, profile_id)

    if jobs is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    return jobs
