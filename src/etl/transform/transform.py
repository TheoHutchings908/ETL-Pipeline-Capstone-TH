import logging
from pathlib import Path
import pandas as pd
from utils.logging_utils import setup_logger

logger = setup_logger(__name__, "transforming_data.log", level=logging.DEBUG)


def load_population_monthly() -> pd.DataFrame:
    POP_PATH = Path(__file__).resolve().parents[3] / "data" / "population.csv"
    pop = (
        pd.read_csv(POP_PATH, parse_dates=["date"])
        .sort_values("date")
        .reset_index(drop=True)
    )
    logger.info(f"Loaded population: {len(pop)} rows")
    return pop


def transform_sales(df_raw: pd.DataFrame) -> pd.DataFrame:
    from etl.transform.clean_sales import (
        clean_dates, clean_strings, drop_empty, fill_numeric, drop_duplicates
    )
    df = (
        df_raw
        .pipe(clean_dates)
        .pipe(clean_strings)
        .pipe(drop_empty)
        .pipe(fill_numeric)
        .pipe(drop_duplicates)
    )
    df["year"] = df["Date"].dt.year
    df = df.drop(columns="year")
    df = df.rename(columns={
        "Date": "date",
        "Car Make": "make",
        "Car Model": "model",
        "Car Price": "price",
    })
    logger.info(f"Transformed sales: {df.shape[0]} rows")
    return df
