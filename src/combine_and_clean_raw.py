import os
import glob
import pandas as pd

RAW_DIR = "data/raw/"
OUTPUT_CSV = os.path.join(RAW_DIR, "hdb_resale_raw.csv")

# Find all CSVs in raw folder (e.g. resale-flat-prices-*.csv)
csv_files = glob.glob(os.path.join(RAW_DIR, "*.csv"))

if not csv_files:
    print(f"No CSV files found in {RAW_DIR}. Please place your raw CSVs there.")
    exit(1)

print(f"Found {len(csv_files)} CSV files: {csv_files}")

# Read and concatenate all CSVs
dfs = []
for f in csv_files:
    df = pd.read_csv(f)
    dfs.append(df)

# Union of all columns
all_cols = set()
for df in dfs:
    all_cols.update(df.columns)
all_cols = list(all_cols)

# Reindex all DataFrames to have all columns (missing columns will be NaN)
dfs = [df.reindex(columns=all_cols) for df in dfs]

# Concatenate and sort by month
df_all = pd.concat(dfs, ignore_index=True)
df_all = df_all.sort_values("month")

# Derive 'remaining_lease' if missing, using lease_commence_date and month
def derive_remaining_lease(row):
    if pd.notnull(row.get('remaining_lease')):
        return row['remaining_lease']
    if pd.notnull(row.get('lease_commence_date')) and pd.notnull(row.get('month')):
        try:
            year = int(str(row['month'])[:4])
            lease_start = int(row['lease_commence_date'])
            lease_years_left = 99 - (year - lease_start)
            return f"{lease_years_left} years"
        except Exception:
            return None
    return None
if 'remaining_lease' not in df_all.columns or df_all['remaining_lease'].isnull().any():
    df_all['remaining_lease'] = df_all.apply(derive_remaining_lease, axis=1)

# Drop duplicates
before = len(df_all)
df_all = df_all.drop_duplicates()
after = len(df_all)
print(f"Dropped {before - after} duplicate rows.")

# Basic cleaning: drop rows with nulls in key columns
key_cols = ["month", "town", "flat_type", "resale_price", "floor_area_sqm"]
missing_keys = [col for col in key_cols if col not in df_all.columns]
if missing_keys:
    print(f"Warning: Missing key columns: {missing_keys}")
else:
    before = len(df_all)
    df_all = df_all.dropna(subset=key_cols)
    after = len(df_all)
    print(f"Dropped {before - after} rows with nulls in key columns.")

# Save combined CSV
df_all.to_csv(OUTPUT_CSV, index=False)
print(f"Combined and cleaned CSV saved to {OUTPUT_CSV} ({len(df_all)} rows)")
