from sqlalchemy import inspect
from app.database import engine

inspector = inspect(engine)

print("Tables:", inspector.get_table_names())

print("\nJobs table columns:")

for column in inspector.get_columns("jobs"):
    print(f"- {column['name']}: {column['type']}")