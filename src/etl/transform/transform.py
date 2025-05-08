from pathlib import Path
import pandas as pd
import logging
from etl.extract.extract import extract_data
from utils.logging_utils import setup_logger
from etl.transform.clean_sales import (
    clean_dates,
    clean_strings,
    drop_empty,
    fix_car_typos,
    fill_numeric,
    drop_duplicates,
)


logger = setup_logger(__name__, "transforming_data.log", level=logging.DEBUG)


POP_PATH = Path(__file__).resolve().parents[3] / "data" / "population.csv"
pop_df = pd.read_csv(POP_PATH)
pop_df["year"] = pop_df["Year"].astype(int)
pop_df = pop_df[["year", "population"]]


def transform_sales(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = (
        df_raw
        .pipe(clean_dates)      
        .pipe(clean_strings)
        .pipe(drop_empty)
        .pipe(fix_car_typos)
        .pipe(fill_numeric)
        .pipe(drop_duplicates)
    )

    df["year"] = df["Date"].dt.year
    df = df.merge(pop_df, on="year", how="left")
    df = df.drop(columns="year")

    logger.info(f"After merge with population: {df.shape[0]} rows, {df.shape[1]} cols")
    return df


# if __name__ == "__main__":
#     raw    = extract_data()
#     merged = transform_sales(raw)
#     out    = Path(__file__).resolve().parents[3] / "data" / "car_sales_enriched.csv"
#     merged.to_csv(out, index=False)
#     logger.info(f"Wrote enriched CSV to {out}")
