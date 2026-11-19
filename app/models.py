from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


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