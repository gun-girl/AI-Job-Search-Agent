from sqlalchemy import inspect

from app import models
from app.database import Base, engine


# Create any tables that do not already exist
Base.metadata.create_all(bind=engine)

# Inspect the database
inspector = inspect(engine)

print("Database tables:")

for table in inspector.get_table_names():
    print(f"\n{table}")

    for column in inspector.get_columns(table):
        print(f"  - {column['name']}: {column['type']}")