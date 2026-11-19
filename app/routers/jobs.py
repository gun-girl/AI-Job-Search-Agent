
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import JobCreate, JobResponse
from app.services import job_service


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# Get all jobs
@router.get("/", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return job_service.get_all_jobs(db)


# Get one job
@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = job_service.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


# Create a job
@router.post("/", response_model=JobResponse, status_code=201)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    return job_service.create_job(db, job_data)


# Update a job
@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    job = job_service.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job_service.update_job(db, job, job_data)


# Delete a job
@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = job_service.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    job_service.delete_job(db, job)

    return {
        "message": "Job deleted successfully",
        "job_id": job_id
    }
