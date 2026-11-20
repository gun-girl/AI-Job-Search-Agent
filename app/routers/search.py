from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import JobResponse
from app.services import search_service


router = APIRouter(
    prefix="/search",
    tags=["Job Search"]
)


@router.get("/jobs", response_model=list[JobResponse])
def search_jobs(
    title: str | None = None,
    keyword: str | None = None,
    location: str | None = None,
    db: Session = Depends(get_db)
):
    return search_service.search_jobs(
        db=db,
        title=title,
        keyword=keyword,
        location=location
    )