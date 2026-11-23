from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


# Fields required when creating a job
class JobCreate(BaseModel):
    title: str
    company: str
    location: str | None = None

    country: str | None = None
    city: str | None = None

    job_category: str | None = None

    experience_level: str | None = None
    employment_type: str | None = None
    work_mode: str | None = None

    required_languages: list[str] = Field(default_factory=list)

    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = "EUR"

    application_deadline: datetime | None = None

    description: str | None = None
    requirements: str | None = None

    application_url: str | None = None
    source: str | None = None


# Fields returned when reading a job
class JobResponse(JobCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)




class CandidateProfileCreate(BaseModel):
    professional_summary: str | None = None
    education: str | None = None
    experience: str | None = None

    skills: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)

    # Flexible job preferences
    preferred_job_titles: list[str] = Field(default_factory=list)
    preferred_job_categories: list[str] = Field(default_factory=list)
    preferred_keywords: list[str] = Field(default_factory=list)

    # Location preferences
    preferred_countries: list[str] = Field(default_factory=list)
    preferred_cities: list[str] = Field(default_factory=list)

    # Required filters
    experience_levels: list[str] = Field(default_factory=list)
    employment_types: list[str] = Field(default_factory=list)
    work_modes: list[str] = Field(default_factory=list)

    # Salary preferences
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str = "EUR"

    # Email notification settings
    email: EmailStr | None = None
    email_notifications_enabled: bool = False
    minimum_match_score: int = Field(default=75, ge=0, le=100)


class CandidateProfileResponse(CandidateProfileCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobMatchResponse(BaseModel):
    job: JobResponse

    match_score: int

    matched_skills: list[str]
    missing_skills: list[str]

    title_match: bool
    experience_match: bool | None

    employment_type_match: bool | None
    work_mode_match: bool | None

    language_match: bool | None
    matched_languages: list[str]
    missing_languages: list[str]

    salary_match: bool | None

    explanations: list[str]


class AIJobEvaluationResult(BaseModel):
    profile_id: int
    job_id: int

    match_score: int
    summary: str

    matched_requirements: list[str]
    missing_requirements: list[str]

    strengths: list[str]
    concerns: list[str]

    recommendation: str


class AIJobEvaluationResponse(AIJobEvaluationResult):
    id: int
    evaluated_at: datetime

    model_config = ConfigDict(from_attributes=True)