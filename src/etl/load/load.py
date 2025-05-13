import os
import pandas as pd
from sqlalchemy import create_engine
from utils.logging_utils import setup_logger

logger = setup_logger(__name__, "load_data.log")


def get_engine():
    return create_engine(os.environ["DATABASE_URL"], echo=False)


def write_table(df: pd.DataFrame, table_name: str):
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    logger.info(f"Wrote {len(df)} rows to '{table_name}' @ Postgres")


def write_sales(df: pd.DataFrame):
    write_table(df, table_name="sales")


def write_population(df: pd.DataFrame):
    write_table(df, table_name="population")
