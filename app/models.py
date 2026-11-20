from sqlalchemy import Column, Integer, String, Text, DateTime
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

    preferred_job_titles = Column(JSON, default=list, nullable=False)
    preferred_countries = Column(JSON, default=list, nullable=False)
    preferred_cities = Column(JSON, default=list, nullable=False)

    experience_level = Column(String(100), nullable=True)

    employment_types = Column(JSON, default=list, nullable=False)
    work_modes = Column(JSON, default=list, nullable=False)

    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(10), default="EUR")

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

    created_at = Column(DateTime(timezone=True), server_default=func.now())