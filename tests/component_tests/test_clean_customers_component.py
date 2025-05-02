import os
import pandas as pd
from etl.transform.clean_customers import clean_customers


def test_clean_customers():
    base_path = os.path.dirname(__file__)
    test_data_path = os.path.join(base_path, '../test_data/test_customers.csv')
    expected_data_path = os.path.join(
        base_path,
        '../test_data/expected_customers_clean_results.csv'
    )

    df = pd.read_csv(test_data_path)
    expected_df = pd.read_csv(expected_data_path)

    result = clean_customers(df)

    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)
