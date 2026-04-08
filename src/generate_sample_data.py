"""
Generate a realistic synthetic HDB resale flat price dataset for development
and demonstration purposes.

The generated data mirrors the key trends in actual Singapore HDB resale prices:
  - Steady price growth from 1990 to 2013
  - Moderate decline from 2013 to 2019 (cooling measures)
  - Sharp surge from 2020 to 2022 (COVID-era demand shock)
  - Elevated plateau from 2023 onwards

Usage:
    python src/generate_sample_data.py
"""

import os
import random
import numpy as np
import pandas as pd

RANDOM_SEED = 42
N_ROWS = 50_000
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUT_FILE = os.path.join(DATA_DIR, "resale_flat_prices_sample.csv")

# ── Town definitions (mature / non-mature) ───────────────────────────────────
TOWNS = {
    # Town name: base price multiplier
    "ANG MO KIO": 1.10,
    "BEDOK": 1.08,
    "BISHAN": 1.25,
    "BUKIT BATOK": 0.95,
    "BUKIT MERAH": 1.30,
    "BUKIT PANJANG": 0.92,
    "BUKIT TIMAH": 1.40,
    "CENTRAL AREA": 1.50,
    "CHOA CHU KANG": 0.88,
    "CLEMENTI": 1.18,
    "GEYLANG": 1.05,
    "HOUGANG": 0.95,
    "JURONG EAST": 0.98,
    "JURONG WEST": 0.90,
    "KALLANG/WHAMPOA": 1.20,
    "MARINE PARADE": 1.35,
    "PASIR RIS": 0.93,
    "PUNGGOL": 0.87,
    "QUEENSTOWN": 1.32,
    "SEMBAWANG": 0.85,
    "SENGKANG": 0.88,
    "SERANGOON": 1.12,
    "TAMPINES": 1.00,
    "TOA PAYOH": 1.28,
    "WOODLANDS": 0.82,
    "YISHUN": 0.85,
}

FLAT_TYPES = {
    "1 ROOM":    0.40,
    "2 ROOM":    0.55,
    "3 ROOM":    0.75,
    "4 ROOM":    1.00,
    "5 ROOM":    1.28,
    "EXECUTIVE": 1.50,
    "MULTI-GENERATION": 1.65,
}

FLAT_TYPE_AREAS = {
    "1 ROOM":    (33, 45),
    "2 ROOM":    (45, 60),
    "3 ROOM":    (60, 80),
    "4 ROOM":    (80, 105),
    "5 ROOM":    (105, 133),
    "EXECUTIVE": (130, 165),
    "MULTI-GENERATION": (155, 175),
}

FLAT_TYPE_WEIGHTS = [0.01, 0.04, 0.25, 0.38, 0.22, 0.09, 0.01]

STOREY_RANGES = [
    "01 TO 03", "04 TO 06", "07 TO 09", "10 TO 12", "13 TO 15",
    "16 TO 18", "19 TO 21", "22 TO 24", "25 TO 27", "28 TO 30",
    "31 TO 33", "34 TO 36", "37 TO 39", "40 TO 42", "43 TO 45",
    "46 TO 48", "49 TO 51",
]

STOREY_MULTIPLIER = {rng: 1.0 + 0.008 * i for i, rng in enumerate(STOREY_RANGES)}


def price_index(year: int, month: int) -> float:
    """Return a macro price index for the given year/month (Jan 1990 = 1.0)."""
    t = year + (month - 1) / 12.0

    # Piecewise trend: growth → peak → cooling → surge → plateau
    if t < 1997.5:          # Pre-AFC boom
        idx = 0.60 + 0.055 * (t - 1990)
    elif t < 1998.5:        # Asian financial crisis dip
        idx = 1.015 - 0.12 * (t - 1997.5)
    elif t < 2008.0:        # Recovery and growth
        idx = 0.895 + 0.030 * (t - 1998.5)
    elif t < 2009.0:        # GFC dip
        idx = 1.175 - 0.08 * (t - 2008.0)
    elif t < 2013.5:        # Post-GFC surge
        idx = 1.095 + 0.085 * (t - 2009.0)
    elif t < 2019.5:        # Cooling measures correction
        idx = 1.478 - 0.020 * (t - 2013.5)
    elif t < 2020.5:        # COVID trough
        idx = 1.358 - 0.015 * (t - 2019.5)
    elif t < 2023.0:        # Post-COVID surge
        idx = 1.343 + 0.120 * (t - 2020.5)
    else:                   # Elevated plateau
        idx = 1.643 + 0.010 * (t - 2023.0)

    return max(idx, 0.30)


def base_price(flat_type: str, area_sqm: float) -> float:
    """Return a base price (before macro & location adjustments) in SGD."""
    price_per_sqm = 2_800  # circa 2005 4-room baseline
    type_mult = FLAT_TYPES[flat_type]
    return price_per_sqm * area_sqm * type_mult


def generate_dataset(n: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    random.seed(seed)

    town_names = list(TOWNS.keys())
    town_mults = list(TOWNS.values())
    flat_type_names = list(FLAT_TYPES.keys())

    rows = []
    for _ in range(n):
        year = int(rng.integers(1990, 2025))
        month = int(rng.integers(1, 13))

        town = rng.choice(town_names)
        loc_mult = TOWNS[town]

        flat_type = rng.choice(flat_type_names, p=FLAT_TYPE_WEIGHTS)
        area_min, area_max = FLAT_TYPE_AREAS[flat_type]
        area = round(float(rng.uniform(area_min, area_max)), 1)

        storey = random.choice(STOREY_RANGES)
        storey_mult = STOREY_MULTIPLIER[storey]

        p_idx = price_index(year, month)
        price = base_price(flat_type, area) * loc_mult * p_idx * storey_mult
        # Add ~5% random noise
        price *= float(rng.normal(1.0, 0.05))
        price = max(int(round(price, -3)), 50_000)

        lease_start = int(rng.integers(max(1966, year - 40), year))
        remaining_years = 99 - (year - lease_start)

        rows.append({
            "month": f"{year}-{month:02d}",
            "town": town,
            "flat_type": flat_type,
            "storey_range": storey,
            "floor_area_sqm": area,
            "flat_model": "Model A",
            "lease_commence_date": lease_start,
            "remaining_lease": f"{remaining_years} years",
            "resale_price": price,
        })

    return pd.DataFrame(rows)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Generating {N_ROWS:,} synthetic records …")
    df = generate_dataset(N_ROWS, RANDOM_SEED)
    df.to_csv(OUT_FILE, index=False)
    print(f"Saved → {OUT_FILE}")
    print(df.describe())


if __name__ == "__main__":
    main()
