# import necessary libraries
from pathlib import Path
import pandas as pd
import logging
import timeit
from utils.logging_utils import setup_logger, log_extract_success

# Configure the logger
logger = setup_logger(
    __name__,
    'extract_data.log',
    level=logging.DEBUG
)

# Set the expected performance threshold (in seconds)
EXPECTED_PERFORMANCE = 0.0001

# Set the path to the CSV file
BASE_DIR = Path(__file__).resolve().parents[3]
FILE_PATH = BASE_DIR / 'data' / 'car_sales_data.csv'


TYPE = 'csv'


# extracts data from csv
def extract_data() -> pd.DataFrame:
    start_time = timeit.default_timer()
    try:
        raw = pd.read_csv(FILE_PATH)
        extract_sales_execution_time = timeit.default_timer() - start_time
        log_extract_success(
            logger,
            TYPE,
            raw.shape,
            extract_sales_execution_time,
            EXPECTED_PERFORMANCE
        )
        return raw
    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Error loading {FILE_PATH}: {e}")
        raise Exception(f"Failed to load CSV file: {FILE_PATH}")