import os
import pandas as pd
from sqlalchemy import create_engine


def get_engine():
    return create_engine(os.environ["DATABASE_URL"], echo=False)


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
