
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CandidateProfile
from app.services.email_service import send_test_email


router = APIRouter(
    prefix="/email-notifications",
    tags=["Email Notifications"],
)


@router.post("/test/{profile_id}")
def test_profile_email(
    profile_id: int,
    db: Session = Depends(get_db),
):
    # Find the profile in the database
    profile = (
        db.query(CandidateProfile)
        .filter(CandidateProfile.id == profile_id)
        .first()
    )

    # Check if the profile exists
    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    # Check if the profile has an email address
    if not profile.email:
        raise HTTPException(
            status_code=400,
            detail="This profile does not have an email address.",
        )

    # Try sending a test email
    try:
        send_test_email(profile.email)

        return {
            "message": "Test email sent successfully.",
            "profile_id": profile.id,
            "recipient": profile.email,
        }

    except Exception as error:
        # Show the error type in the VS Code terminal
        # without exposing passwords or SMTP credentials
        print(
            "EMAIL ERROR TYPE:",
            type(error).__name__,
            flush=True,
        )

        raise HTTPException(
            status_code=502,
            detail="Email sending failed. Check VS Code terminal.",
        )
