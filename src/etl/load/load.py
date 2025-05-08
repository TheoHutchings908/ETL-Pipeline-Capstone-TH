import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from utils.logging_utils import setup_logger

logger = setup_logger(__name__, "load_data.log")

load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST','localhost')}:"
    f"{os.getenv('POSTGRES_PORT','5432')}/"
    f"{os.getenv('POSTGRES_DB')}"
)


_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DB_URL, echo=False)
    return _engine


def write_data(df: pd.DataFrame, table_name: str = "sales"):
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    logger.info(f"Wrote {len(df)} rows to {table_name}@Postgres")

