from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Job


def search_jobs(
    db: Session,
    title: str | None = None,
    keyword: str | None = None,
    location: str | None = None
):
    query = db.query(Job)

    # Filter by job title
    if title:
        query = query.filter(Job.title.ilike(f"%{title}%"))

    # Search across several job fields
    if keyword:
        keyword_filter = f"%{keyword}%"

        query = query.filter(
            or_(
                Job.title.ilike(keyword_filter),
                Job.company.ilike(keyword_filter),
                Job.description.ilike(keyword_filter),
                Job.requirements.ilike(keyword_filter)
            )
        )

    # Filter by location
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    return query.order_by(Job.id.desc()).all()