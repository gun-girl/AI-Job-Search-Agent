from sqlalchemy import inspect, text

from app import models
from app.database import engine


# New columns to add to the existing jobs table
new_columns = {
    "employment_type": "VARCHAR(100)",
    "work_mode": "VARCHAR(100)",
    "experience_level": "VARCHAR(100)",
    "required_languages": "JSON NOT NULL DEFAULT '[]'",
    "salary_min": "INTEGER",
    "salary_max": "INTEGER",
    "salary_currency": "VARCHAR(10) DEFAULT 'EUR'",
    "application_deadline": "DATETIME",
    "published_at": "DATETIME",
}


inspector = inspect(engine)
existing_columns = {
    column["name"]
    for column in inspector.get_columns("jobs")
}


with engine.begin() as connection:
    for column_name, column_type in new_columns.items():
        if column_name not in existing_columns:
            connection.execute(
                text(
                    f"ALTER TABLE jobs ADD COLUMN "
                    f"{column_name} {column_type}"
                )
            )
            print(f"Added column: {column_name}")
        else:
            print(f"Already exists: {column_name}")


# Create any other missing tables
models.Base.metadata.create_all(bind=engine)

print("\nDatabase update completed.")