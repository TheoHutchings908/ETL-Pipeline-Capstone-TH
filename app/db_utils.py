import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


def get_engine():
    url = os.getenv("DATABASE_URL") or (
        f"postgresql://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )
    return create_engine(url, echo=False)


def get_available_years() -> list[int]:
    engine = get_engine()
    sql = """
        SELECT DISTINCT
            EXTRACT(YEAR FROM date)::INT AS year
        FROM sales
        ORDER BY year
    """
    df = pd.read_sql(sql, engine)
    return df["year"].tolist()


def load_all_sales() -> pd.DataFrame:
    engine = get_engine()
    df = pd.read_sql(
        "SELECT * FROM sales",
        engine,
        parse_dates=["date"]
    )
    return df
