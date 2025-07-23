# db/load_data.py
import pandas as pd
from sqlalchemy import create_engine

def load_data():
    engine = create_engine("sqlite:///db/database.db")

    sheets = {
        "ads": "data/Product-Level Ad Sales and Metrics (mapped).csv",
        "eligibility": "data/Product-Level Eligibility Table (mapped).csv",
        "sales": "data/Product-Level Total Sales and Metrics (mapped).csv"
    }

    for table_name, filepath in sheets.items():
        df = pd.read_csv(filepath)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"[+] Loaded '{table_name}' with {len(df)} rows from {filepath}")

if __name__ == "__main__":
    load_data()
