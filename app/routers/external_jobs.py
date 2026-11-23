
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.jobicy_service import import_jobicy_jobs


router = APIRouter(
    prefix="/external-jobs",
    tags=["External Job Sources"],
)


@router.post("/import/jobicy")
def import_from_jobicy(
    db: Session = Depends(get_db),
):
    try:
        return import_jobicy_jobs(db)

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=502,
            detail=f"Jobicy import failed: {str(error)}",
        )
