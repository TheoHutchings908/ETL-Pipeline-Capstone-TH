import os
import pandas as pd
from sqlalchemy import create_engine
from utils.logging_utils import setup_logger


engine = create_engine(os.environ["DATABASE_URL"], echo=False)

logger = setup_logger(__name__, "load_data.log")

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:" 
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST', 'localhost')}:" 
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DB_URL, echo=False)
    return _engine


def write_table(df: pd.DataFrame, table_name: str):
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    logger.info(f"Wrote {len(df)} rows to '{table_name}' @ Postgres")


def write_sales(df: pd.DataFrame):
    write_table(df, table_name="sales")


def write_population(df: pd.DataFrame):
    write_table(df, table_name="population")
