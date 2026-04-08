"""
Fetch HDB resale flat price data from the Singapore government's open data portal
(data.gov.sg) and save it locally as CSV files.

Dataset IDs (resource IDs from data.gov.sg):
  - 1990–1999 : d_43f493c6c50d54243cc1eab0df142d6b
  - 2000–2012 : d_2d5ff9ea31397b66239f245f57751537
  - 2012–2014 : d_ea9ed51da2787afaf8e51f0f6dce8445
  - 2015–2016 : d_db5571a4b33e98b64e7b54f7f48b8fc2
  - 2017 onwards: d_8b84c4ee58e3cfc0ece0d773c8ca6abc

Usage:
    python src/fetch_data.py
"""

import os
import time
import requests
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

DATASETS = {
    "resale_1990_1999": "d_43f493c6c50d54243cc1eab0df142d6b",
    "resale_2000_2012": "d_2d5ff9ea31397b66239f245f57751537",
    "resale_2012_2014": "d_ea9ed51da2787afaf8e51f0f6dce8445",
    "resale_2015_2016": "d_db5571a4b33e98b64e7b54f7f48b8fc2",
    "resale_2017_onwards": "d_8b84c4ee58e3cfc0ece0d773c8ca6abc",
}

BASE_URL = "https://data.gov.sg/api/action/datastore_search"
RECORDS_PER_REQUEST = 10000


def fetch_dataset(resource_id: str, name: str) -> pd.DataFrame:
    """Download all records for a given resource_id via pagination."""
    records = []
    offset = 0
    total = None

    print(f"  Fetching '{name}' (resource_id={resource_id}) …", flush=True)

    while True:
        params = {
            "resource_id": resource_id,
            "limit": RECORDS_PER_REQUEST,
            "offset": offset,
        }
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()

        payload = resp.json()
        if not payload.get("success"):
            raise RuntimeError(f"API returned success=false for {resource_id}")

        result = payload["result"]
        if total is None:
            total = result["total"]
            print(f"    Total records: {total:,}")

        batch = result["records"]
        if not batch:
            break

        records.extend(batch)
        offset += len(batch)
        print(f"    Downloaded {offset:,} / {total:,} records …", end="\r", flush=True)

        if offset >= total:
            break

        # Be polite to the API
        time.sleep(0.2)

    print()
    return pd.DataFrame(records)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    all_frames = []

    for name, resource_id in DATASETS.items():
        out_path = os.path.join(DATA_DIR, f"{name}.csv")
        if os.path.exists(out_path):
            print(f"  '{name}' already downloaded, skipping.")
            df = pd.read_csv(out_path)
        else:
            df = fetch_dataset(resource_id, name)
            df.to_csv(out_path, index=False)
            print(f"  Saved {len(df):,} rows → {out_path}")
        all_frames.append(df)

    combined = pd.concat(all_frames, ignore_index=True)

    # Normalise column names and drop internal API columns
    combined.drop(columns=["_id"], errors="ignore", inplace=True)

    # Ensure resale_price is numeric
    combined["resale_price"] = pd.to_numeric(combined["resale_price"], errors="coerce")

    combined_path = os.path.join(DATA_DIR, "resale_flat_prices_all.csv")
    combined.to_csv(combined_path, index=False)
    print(f"\nCombined dataset: {len(combined):,} rows → {combined_path}")


if __name__ == "__main__":
    main()
