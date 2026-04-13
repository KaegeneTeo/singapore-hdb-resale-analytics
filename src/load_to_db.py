import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
# Always load .env from project root
from pathlib import Path
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

DB_PARAMS = dict(
    database=os.getenv("MYSQL_DATABASE", "mydb"),
    user=os.getenv("MYSQL_USER", "myuser"),
    password=os.getenv("MYSQL_PASSWORD", "mypass"),
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
)
CSV_PATH = "../data/raw/hdb_resale_raw.csv"
TABLE_NAME = "hdb_resale"


CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    month VARCHAR(16),
    town VARCHAR(64),
    flat_type VARCHAR(32),
    block VARCHAR(16),
    street_name VARCHAR(128),
    storey_range VARCHAR(16),
    floor_area_sqm FLOAT,
    flat_model VARCHAR(64),
    lease_commence_date INT,
    remaining_lease VARCHAR(32),
    resale_price FLOAT
);
"""

INSERT_SQL = f"""
INSERT INTO {TABLE_NAME} (
    month, town, flat_type, block, street_name, storey_range, floor_area_sqm, flat_model, lease_commence_date, remaining_lease, resale_price
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def main():
    if not os.path.exists(CSV_PATH):
        print(f"CSV not found at {CSV_PATH}. Please download and place it there.")
        return
    df = pd.read_csv(CSV_PATH)
    # Clean and validate 'floor_area_sqm' column
    df['floor_area_sqm'] = pd.to_numeric(df['floor_area_sqm'], errors='coerce')
    # Drop rows where floor_area_sqm is NaN or not positive
    df = df.dropna(subset=['floor_area_sqm'])
    df = df[df['floor_area_sqm'] > 0]
    # Debug: print first few values of floor_area_sqm
    print('First 10 floor_area_sqm values:', df['floor_area_sqm'].head(10).tolist())

    # Debug: print MySQL table schema
    conn = mysql.connector.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute(f"DESCRIBE {TABLE_NAME};")
    schema = cur.fetchall()
    print('MySQL table schema:')
    for col in schema:
        print(col)
    cur.close()
    conn.close()

    # Reorder DataFrame columns to match INSERT statement
    insert_columns = [
        'month', 'town', 'flat_type', 'block', 'street_name', 'storey_range',
        'floor_area_sqm', 'flat_model', 'lease_commence_date', 'remaining_lease', 'resale_price'
    ]
    df = df[insert_columns]

    # Reconnect for actual loading
    conn = mysql.connector.connect(**DB_PARAMS)
    cur = conn.cursor()
    conn = mysql.connector.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    # Clear table before loading
    cur.execute(f"TRUNCATE TABLE {TABLE_NAME};")
    conn.commit()
    # Insert data with error handling
    records = df.where(pd.notnull(df), None).values.tolist()
    errors = []
    for idx, record in enumerate(records):
        try:
            cur.execute(INSERT_SQL, record)
        except Exception as e:
            errors.append((idx, record, str(e)))
    conn.commit()
    if errors:
        print(f"Encountered {len(errors)} errors during insertion. Sample errors:")
        for err in errors[:10]:
            print(f"Row {err[0]}: {err[2]}")
    else:
        print("All rows inserted successfully.")
    cur.close()
    conn.close()
    print(f"Loaded {len(df)} rows into {TABLE_NAME}.")

if __name__ == "__main__":
    main()
