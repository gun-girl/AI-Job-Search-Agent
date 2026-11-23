
from sqlalchemy.orm import Session

from app.models import CandidateProfile
from app.schemas import CandidateProfileCreate


# Get all candidate profiles
def get_all_profiles(db: Session):
    return db.query(CandidateProfile).order_by(
        CandidateProfile.id.desc()
    ).all()


# Get one candidate profile by ID
def get_profile_by_id(db: Session, profile_id: int):
    return db.query(CandidateProfile).filter(
        CandidateProfile.id == profile_id
    ).first()


# Create a new candidate profile
def create_profile(db: Session, profile_data: CandidateProfileCreate):
    new_profile = CandidateProfile(**profile_data.model_dump())

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


def update_profile(db: Session, profile_id: int, profile_data):
    profile = get_profile_by_id(db, profile_id)

    if not profile:
        return None

    for field, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile