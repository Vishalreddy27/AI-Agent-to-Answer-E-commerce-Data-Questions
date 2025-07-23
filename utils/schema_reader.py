# utils/schema_reader.py
from sqlalchemy import create_engine, inspect
def get_schema_context():
    engine = create_engine("sqlite:///db/database.db")
    inspector = inspect(engine)
    
    context = "Database schema and sample information:\n"
    for table_name in inspector.get_table_names():
        context += f"\nTable: {table_name}\n"
        columns = inspector.get_columns(table_name)
        for col in columns:
            context += f"  - {col['name']} ({col['type']})\n"
    return context
if __name__ == "__main__":
    print(get_schema_context())