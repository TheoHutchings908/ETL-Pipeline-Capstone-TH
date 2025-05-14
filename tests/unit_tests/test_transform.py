# tests/etl/test_clean_sales.py
import pandas as pd
import numpy as np
import pytest
from etl.transform.clean_sales import drop_duplicates, drop_empty, clean_dates, fill_numeric


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Date": [
            "2021-01-01",
            "2021-01-01",
            None,
            "not a date",
            "2021-02-02"
        ],
        "Sale_Price": [
            10000,
            10000,
            5000,
            20000,
            None
        ],
        "Car_Year": [2010, 2010, 2012, np.nan, 2015],
        "Commission_Rate": [0.05, 0.05, np.nan, 0.1, 0.2],
        "Commission_Earned": [500, 500, 600, np.nan, np.nan],
        "Other": ["keep", "keep", "keep", "keep", "keep"]
    })


def test_drop_duplicates_removes_exact_rows(sample_df):
    deduped = drop_duplicates(sample_df)
    assert len(deduped) == len(sample_df) - 1
    assert deduped.duplicated(keep=False).sum() == 0


def test_drop_empty(sample_df):
    cleaned = drop_empty(sample_df)
    assert len(cleaned) == 3
    assert not cleaned["Date"].isna().any()
    assert not cleaned["Sale_Price"].isna().any()


def test_clean_dates(sample_df):
    dated = clean_dates(sample_df)
    assert pd.api.types.is_datetime64_any_dtype(dated["Date"])
    assert dated.loc[0, "Date"] == pd.Timestamp("2021-01-01")
    assert pd.isna(dated.loc[3, "Date"])


def test_fill_numeric(sample_df):
    medians = sample_df[["Car_Year", "Sale_Price", "Commission_Rate", "Commission_Earned"]].median()
    filled = fill_numeric(sample_df)
    for col in medians.index:
        col_series = filled[col]
        assert not col_series.isna().any()
        assert (col_series == medians[col]).any()


def test_end_to_end_pipeline(sample_df):
    df = (
        sample_df
        .pipe(drop_duplicates)
        .pipe(drop_empty)
        .pipe(clean_dates)
        .pipe(fill_numeric)
    )
    assert len(df) == 2 
    assert df.duplicated(keep=False).sum() == 0
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])
    for col in ["Car_Year", "Sale_Price", "Commission_Rate", "Commission_Earned"]:
        assert not df[col].isna().any()
