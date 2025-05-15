import pandas as pd


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


def drop_empty(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=['Date', 'Sale_Price'])


def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Date'] = pd.to_datetime(
        df['Date'],
        errors='coerce'
    )
    return df


def fill_numeric(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    num_cols = ['Car_Year',
                'Sale_Price',
                'Commission_Rate',
                'Commission_Earned']
    for col in num_cols:
        median = df[col].median()
        df[col] = df[col].fillna(median)
    return df
