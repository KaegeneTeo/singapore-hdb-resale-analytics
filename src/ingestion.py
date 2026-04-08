import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from pathlib import Path

RAW_CSV_PATH = Path("data/raw/hdb_resale_raw.csv")
RAW_PARQUET_PATH = Path("data/raw/hdb_resale_raw.parquet")

def fetch_hdb_resale_data():
    """
    Load HDB resale data from PostgreSQL if available, else from CSV, else raise error.
    """
    # Try DB first
    db_url = os.getenv("DATABASE_URL", "postgresql://hdbuser:hdbpass@localhost:5432/hdbresale")
    try:
        engine = create_engine(db_url)
        df = pd.read_sql_table("hdb_resale", engine)
        # Save as parquet for fast reload
        RAW_PARQUET_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(RAW_PARQUET_PATH, index=False)
        print(f"Loaded {len(df)} rows from PostgreSQL.")
        return df
    except Exception as e:
        print(f"Could not load from DB: {e}")
    # Fallback to CSV
    if RAW_CSV_PATH.exists():
        df = pd.read_csv(RAW_CSV_PATH)
        RAW_PARQUET_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(RAW_PARQUET_PATH, index=False)
        print(f"Loaded {len(df)} rows from CSV.")
        return df
    raise FileNotFoundError("No data found in DB or CSV. Please download the CSV and/or load to DB.")

if __name__ == "__main__":
    df = fetch_hdb_resale_data()
    print(f"Fetched {len(df)} rows. Saved to {RAW_PARQUET_PATH}.")
