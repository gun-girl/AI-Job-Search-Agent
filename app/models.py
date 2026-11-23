from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func

from app.database import Base

from sqlalchemy import JSON


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)

    professional_summary = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)

    skills = Column(JSON, default=list, nullable=False)
    languages = Column(JSON, default=list, nullable=False)

    # Flexible job preferences
    preferred_job_titles = Column(JSON, default=list, nullable=False)
    preferred_job_categories = Column(JSON, default=list, nullable=False)
    preferred_keywords = Column(JSON, default=list, nullable=False)

    # Required location filters
    preferred_countries = Column(JSON, default=list, nullable=False)
    preferred_cities = Column(JSON, default=list, nullable=False)

    # Required filters
    experience_levels = Column(JSON, default=list, nullable=False)
    employment_types = Column(JSON, default=list, nullable=False)
    work_modes = Column(JSON, default=list, nullable=False)

    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(10), default="EUR")

    # Individual notification settings
    email = Column(String(320), nullable=True)
    email_notifications_enabled = Column(Boolean, default=False, nullable=False)
    minimum_match_score = Column(Integer, default=75, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)

    description = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)

    application_url = Column(String(1000), nullable=True)
    source = Column(String(100), nullable=True)

    employment_type = Column(String(100), nullable=True)
    work_mode = Column(String(100), nullable=True)
    experience_level = Column(String(100), nullable=True)

    required_languages = Column(JSON, default=list, nullable=False)

    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(10), default="EUR")

    application_deadline = Column(DateTime(timezone=True), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)

    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)

    job_category = Column(String(100), nullable=True)

    experience_level = Column(String(100), nullable=True)
    employment_type = Column(String(100), nullable=True)
    work_mode = Column(String(100), nullable=True)

    required_languages = Column(JSON, default=list, nullable=False)

    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(10), nullable=True)

    application_deadline = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AIJobEvaluation(Base):
    __tablename__ = "ai_job_evaluations"

    id = Column(Integer, primary_key=True, index=True)

    profile_id = Column(Integer, nullable=False)
    job_id = Column(Integer, nullable=False)

    match_score = Column(Integer, nullable=False)
    summary = Column(Text, nullable=False)

    matched_requirements = Column(JSON, default=list, nullable=False)
    missing_requirements = Column(JSON, default=list, nullable=False)

    strengths = Column(JSON, default=list, nullable=False)
    concerns = Column(JSON, default=list, nullable=False)

    recommendation = Column(String(100), nullable=False)

    evaluated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )