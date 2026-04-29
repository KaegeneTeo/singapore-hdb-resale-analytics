import pandas as pd
import numpy as np
from pathlib import Path
import re

RAW_PATH = Path("data/raw/hdb_resale_raw.parquet")
PROC_PATH = Path("data/processed/hdb_resale_processed.parquet")


def parse_storey_mid(storey_range):
    if pd.isna(storey_range):
        return np.nan
    match = re.match(r"(\d+) TO (\d+)", str(storey_range))
    if match:
        low, high = map(int, match.groups())
        return (low + high) // 2
    return np.nan

def parse_remaining_lease(lease):
    if pd.isna(lease):
        return np.nan
    match = re.match(r"(\d+) years?(?: (\d+) months?)?", str(lease))
    if match:
        years = int(match.group(1))
        months = int(match.group(2) or 0)
        return years + months / 12
    return np.nan

def transform_hdb_data(df):
    df = df.copy()
    # 1. Parse month
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m")
    # 2. Extract year, quarter
    df["year"] = df["month"].dt.year
    df["quarter"] = df["month"].dt.to_period("Q").astype(str)
    # 3. Standardize town, flat_type
    df["town"] = df["town"].str.title()
    df["flat_type"] = df["flat_type"].str.title()
    # 4. price_per_sqm
    df["price_per_sqm"] = df["resale_price"] / df["floor_area_sqm"]
    # 5. storey_mid
    df["storey_mid"] = df["storey_range"].apply(parse_storey_mid)
    # 6. remaining_lease_years
    df["remaining_lease_years"] = df["remaining_lease"].apply(parse_remaining_lease)
    # 7. Drop nulls
    df = df.dropna(subset=["resale_price", "floor_area_sqm", "town"])
    # 8. Save
    PROC_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PROC_PATH, index=False)
    return df

if __name__ == "__main__":
    if RAW_PATH.exists():
        df = pd.read_parquet(RAW_PATH)
    else:
        csv_path = Path("data/raw/hdb_resale_raw.csv")
        if csv_path.exists():
            print("Parquet file not found, reading from CSV instead...")
            df = pd.read_csv(csv_path)
        else:
            raise FileNotFoundError("Neither Parquet nor CSV raw data file found in data/raw/.")
    df_clean = transform_hdb_data(df)
    print(f"Transformed data: {len(df_clean)} rows. Saved to {PROC_PATH}.")
