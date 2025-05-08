# app/db_utils.py
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
          EXTRACT(YEAR FROM "Date")::INT AS year
        FROM sales
        ORDER BY year
    """
    df = pd.read_sql(sql, engine)
    return df["year"].tolist()


def load_sales(year: int) -> pd.DataFrame:
    sql = """
    SELECT
      "Date"            AS date,
      "Car Make"        AS make,
      "Car Model"       AS model,
      "Sale Price"      AS sale_price,
      "Commission Earned" AS commission_earned,
      population
    FROM sales
    WHERE EXTRACT(YEAR FROM "Date") = %(year)s
    ORDER BY "Date"
    """
    engine = get_engine()
    df = pd.read_sql(
        sql,
        engine,
        params={"year": year},
        parse_dates=["date"],
    )
    return df