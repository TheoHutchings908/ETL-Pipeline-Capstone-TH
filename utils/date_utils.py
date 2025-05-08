import pandas as pd


def standardise_date(date_str):
    if pd.isna(date_str) or date_str == '':
        return pd.NaT

    formats = [
        '%Y/%m/%d', '%Y-%m-%d', '%d %b %Y', '%b %d, %Y', '%d %B %Y',
        '%d-%m-%Y', '%d/%m/%Y'
    ]
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue

    return pd.NaT