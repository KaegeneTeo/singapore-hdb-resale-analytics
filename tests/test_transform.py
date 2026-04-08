import pytest
import pandas as pd
from src.transform import transform_hdb_data

def test_transform_hdb_data(tmp_path):
    # Minimal fake data
    df = pd.DataFrame({
        "month": ["2024-01"],
        "town": ["ANG MO KIO"],
        "flat_type": ["4 ROOM"],
        "resale_price": [500000],
        "floor_area_sqm": [100],
        "storey_range": ["10 TO 12"],
        "remaining_lease": ["90 years"]
    })
    df_clean = transform_hdb_data(df)
    assert "price_per_sqm" in df_clean.columns
    assert "storey_mid" in df_clean.columns
    assert "remaining_lease_years" in df_clean.columns
    assert df_clean["price_per_sqm"].iloc[0] == 5000
    assert df_clean["storey_mid"].iloc[0] == 11
    assert df_clean["remaining_lease_years"].iloc[0] == 90
