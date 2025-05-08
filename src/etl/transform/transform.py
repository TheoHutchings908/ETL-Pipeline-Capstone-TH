from pathlib import Path
from etl.extract.extract import extract_data
from utils.logging_utils import setup_logger
import logging
from etl.transform.clean_sales import (
    clean_dates,
    clean_strings,
    drop_empty,
    fix_car_typos,
    fill_numeric,
    drop_duplicates,
)

logger = setup_logger(
    __name__,
    'transforming_data.log',
    level=logging.DEBUG
)


def main():
    sales = extract_data()

    sales_clean = (
        sales
        .pipe(clean_dates)
        .pipe(clean_strings)
        .pipe(drop_empty)
        .pipe(fix_car_typos)
        .pipe(fill_numeric)
        .pipe(drop_duplicates)
    )
    
    logger.info(f"Cleaning complete: {sales_clean.shape[0]} rows, {sales_clean.shape[1]} cols")

    out_path = Path(__file__).resolve().parents[3] / "data" / "car_sales_clean.csv"
    sales_clean.to_csv(out_path, index=False)


if __name__ == "__main__":
    main()