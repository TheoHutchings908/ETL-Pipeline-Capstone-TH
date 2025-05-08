import sys, os
from dotenv import load_dotenv
import logging
from etl.extract.extract import extract_data
from etl.transform.transform import transform_sales
from etl.load.load import write_data

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

load_dotenv()

logging.basicConfig(filename="logs/etl.log", level=logging.INFO)


def main():
    raw = extract_data()
    clean = transform_sales(raw)
    write_data(clean)


if __name__ == "__main__":
    main()
