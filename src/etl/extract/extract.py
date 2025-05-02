import os
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

EXPECTED_PERFORMANCE = 0.0001

FILE_PATH = os.path.join(
    os.path.dirname(__file__), '../../data/car_sales_data.csv'
)

TYPE = 'csv'  


def extract_data() -> pd.DataFrame:
    start_time = timeit.default_timer()
    
    try:
        sales = pd.read_csv(FILE_PATH)
        extract_sales_execution_time = timeit.default_timer() - start_time
        log_extract_success(
            logger,
            TYPE,
            sales.shape,
            extract_sales_execution_time,
            EXPECTED_PERFORMANCE
        )
        return sales
    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Error loading {FILE_PATH}: {e}")
        raise Exception(f"Failed to load CSV file: {FILE_PATH}")
    