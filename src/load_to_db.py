import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
load_dotenv()
DB_PARAMS = dict(
    dbname=os.getenv("POSTGRES_DB", "hdbresale"),
    user=os.getenv("POSTGRES_USER", "hdbuser"),
    password=os.getenv("POSTGRES_PASSWORD", "hdbpass"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
)

CSV_PATH = "data/raw/hdb_resale_raw.csv"
TABLE_NAME = "hdb_resale"

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    month TEXT,
    town TEXT,
    flat_type TEXT,
    block TEXT,
    street_name TEXT,
    storey_range TEXT,
    floor_area_sqm FLOAT,
    flat_model TEXT,
    lease_commence_date INT,
    remaining_lease TEXT,
    resale_price FLOAT
);
"""

INSERT_SQL = f"""
INSERT INTO {TABLE_NAME} (
    month, town, flat_type, block, street_name, storey_range, floor_area_sqm, flat_model, lease_commence_date, remaining_lease, resale_price
) VALUES %s
ON CONFLICT DO NOTHING;
"""

def main():
    if not os.path.exists(CSV_PATH):
        print(f"CSV not found at {CSV_PATH}. Please download and place it there.")
        return
    df = pd.read_csv(CSV_PATH)
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    # Clear table before loading
    cur.execute(f"TRUNCATE TABLE {TABLE_NAME};")
    conn.commit()
    # Insert data
    records = df.where(pd.notnull(df), None).values.tolist()
    execute_values(cur, INSERT_SQL, records, page_size=1000)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(df)} rows into {TABLE_NAME}.")

if __name__ == "__main__":
    main()
