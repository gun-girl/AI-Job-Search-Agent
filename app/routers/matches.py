from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import JobMatchResponse
from app.services import job_service, profile_service, matching_service


router = APIRouter(
    prefix="/matches",
    tags=["Job Matching"]
)


# Match all saved jobs against one candidate profile
@router.get("/{profile_id}", response_model=list[JobMatchResponse])
def get_job_matches(profile_id: int, db: Session = Depends(get_db)):
    profile = profile_service.get_profile_by_id(db, profile_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    jobs = job_service.get_all_jobs(db)

    results = [
        matching_service.match_job_to_profile(profile, job)
        for job in jobs
    ]

    results.sort(
        key=lambda result: result["match_score"],
        reverse=True
    )

    return results