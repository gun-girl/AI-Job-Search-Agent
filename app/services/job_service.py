
from sqlalchemy.orm import Session

from app.models import Job
from app.schemas import JobCreate


def get_all_jobs(db: Session):
    return db.query(Job).order_by(Job.id.desc()).all()


def get_job_by_id(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


def create_job(db: Session, job_data: JobCreate):
    new_job = Job(**job_data.model_dump())

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


def update_job(db: Session, job: Job, job_data: JobCreate):
    for field, value in job_data.model_dump().items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


def delete_job(db: Session, job: Job):
    db.delete(job)
    db.commit()
