
from sqlalchemy import inspect, text

from app.database import engine, Base
from app import models


# Columns to add to existing candidate profiles
profile_columns = {
    "email": "VARCHAR(320)",
    "email_notifications_enabled": "BOOLEAN NOT NULL DEFAULT 0",
    "minimum_match_score": "INTEGER NOT NULL DEFAULT 75",
    "preferred_job_categories": "JSON NOT NULL DEFAULT '[]'",
    "preferred_keywords": "JSON NOT NULL DEFAULT '[]'",
    "experience_levels": "JSON NOT NULL DEFAULT '[]'",
}


# Columns to add to existing jobs
job_columns = {
    "country": "VARCHAR(100)",
    "city": "VARCHAR(100)",
    "job_category": "VARCHAR(100)",
    "experience_level": "VARCHAR(100)",
    "employment_type": "VARCHAR(100)",
    "work_mode": "VARCHAR(100)",
    "required_languages": "JSON NOT NULL DEFAULT '[]'",
    "salary_min": "INTEGER",
    "salary_max": "INTEGER",
    "salary_currency": "VARCHAR(10)",
    "application_deadline": "DATETIME",
}


# All database migrations
migrations = {
    "candidate_profiles": profile_columns,
    "jobs": job_columns,
}


def migrate_database():
    with engine.begin() as connection:

        inspector = inspect(connection)

        for table_name, columns in migrations.items():

            existing_columns = {
                column["name"]
                for column in inspector.get_columns(table_name)
            }

            for column_name, column_type in columns.items():

                if column_name not in existing_columns:

                    connection.execute(
                        text(
                            f"ALTER TABLE {table_name} "
                            f"ADD COLUMN {column_name} {column_type}"
                        )
                    )

                    print(f"Added column: {table_name}.{column_name}")

                else:
                    print(f"Already exists: {table_name}.{column_name}")

    # Create any missing tables
    Base.metadata.create_all(bind=engine)

    print("\nDatabase migration completed successfully!")


if __name__ == "__main__":
    migrate_database()
