import pytest
import pandas as pd
from utils.date_utils import standardise_date


@pytest.mark.parametrize("date_str, expected", [
    ('2021/01/01', pd.Timestamp('2021-01-01')),
    ('01-02-2021', pd.Timestamp('2021-02-01')),
    ('2021-03-01', pd.Timestamp('2021-03-01')),
    ('01-04-2021', pd.Timestamp('2021-04-01')),
    ('01 Jan 2021', pd.Timestamp('2021-01-01')),
    ('Jan 01, 2021', pd.Timestamp('2021-01-01')),
    ('01/05/2021', pd.Timestamp('2021-05-01')),
    ('05/01/2021', pd.Timestamp('2021-01-05')),
    ('01 January 2021', pd.Timestamp('2021-01-01')),
    ('invalid date', pd.NaT),
    ('', pd.NaT),
    (None, pd.NaT),
    ('2021/13/01', pd.NaT),  # Invalid month
    ('2021/01/32', pd.NaT),  # Invalid day
    ('2021-02-30', pd.NaT)   # Invalid date
])
def test_standardise_date(date_str, expected):
    result = standardise_date(date_str)
    if pd.isna(expected):
        assert pd.isna(result)
    else:
        assert result == expected
