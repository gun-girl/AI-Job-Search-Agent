from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AIJobEvaluationResponse
from app.services import job_service, profile_service
from app.services import evaluation_service


router = APIRouter(
    prefix="/ai-evaluations",
    tags=["AI Job Evaluations"]
)


# Evaluate a job and save the result
@router.post(
    "/{profile_id}/{job_id}",
    response_model=AIJobEvaluationResponse
)
def evaluate_job(
    profile_id: int,
    job_id: int,
    db: Session = Depends(get_db)
):
    profile = profile_service.get_profile_by_id(
        db,
        profile_id
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    job = job_service.get_job_by_id(
        db,
        job_id
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return evaluation_service.evaluate_job(
        db,
        profile,
        job
    )


# Retrieve previous evaluations for a candidate
@router.get(
    "/profile/{profile_id}",
    response_model=list[AIJobEvaluationResponse]
)
def get_profile_evaluations(
    profile_id: int,
    db: Session = Depends(get_db)
):
    profile = profile_service.get_profile_by_id(
        db,
        profile_id
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    return evaluation_service.get_evaluations_for_profile(
        db,
        profile_id
    )