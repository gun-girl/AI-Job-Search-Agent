
from pathlib import Path

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Find the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Define where our SQLite database will be stored
DATABASE_PATH = BASE_DIR / "job_search.db"

# Create the database connection URL
DATABASE_URL = URL.create(
    drivername="sqlite",
    database=str(DATABASE_PATH)
)

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for our database models
Base = declarative_base()


# Database dependency for FastAPI endpoints
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
