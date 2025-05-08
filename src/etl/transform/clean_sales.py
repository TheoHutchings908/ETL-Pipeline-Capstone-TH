import pandas as pd


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    # Remove exact duplicate rows.
    return df.drop_duplicates()


def drop_empty(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows missing a Date or Sale Price.
    return df.dropna(subset=['Date', 'Sale Price'])


def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Date'] = pd.to_datetime(
        df['Date'],
        errors='coerce'
    )
    return df


def clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    # Trim whitespace and title-case key text columns.
    df = df.copy()
    text_cols = ['Salesperson', 'Customer Name', 'Car Make', 'Car Model']
    for col in text_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.title()
        )
    return df


def fill_numeric(df: pd.DataFrame) -> pd.DataFrame:
    # Fill missing numeric columns with their median.
    df = df.copy()
    num_cols = ['Car Year',
                'Sale Price',
                'Commission Rate',
                'Commission Earned']
    for col in num_cols:
        median = df[col].median()
        df[col] = df[col].fillna(median)
    return df
