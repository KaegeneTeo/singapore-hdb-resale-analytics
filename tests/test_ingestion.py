import pytest
import pandas as pd
from src.ingestion import fetch_hdb_resale_data

def test_fetch_hdb_resale_data_runs():
    df = fetch_hdb_resale_data(max_retries=1)  # Use 1 retry for test speed
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert set(["month", "town", "flat_type"]).issubset(df.columns)
