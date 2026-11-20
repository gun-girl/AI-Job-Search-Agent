
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    CandidateProfileCreate,
    CandidateProfileResponse
)
from app.services import profile_service


router = APIRouter(
    prefix="/profiles",
    tags=["Candidate Profiles"]
)


# Get all candidate profiles
@router.get("/", response_model=list[CandidateProfileResponse])
def get_profiles(db: Session = Depends(get_db)):
    return profile_service.get_all_profiles(db)


# Get one candidate profile
@router.get("/{profile_id}", response_model=CandidateProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = profile_service.get_profile_by_id(db, profile_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    return profile


# Create a candidate profile
@router.post(
    "/",
    response_model=CandidateProfileResponse,
    status_code=201
)
def create_profile(
    profile_data: CandidateProfileCreate,
    db: Session = Depends(get_db)
):
    return profile_service.create_profile(db, profile_data)
