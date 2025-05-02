import os
import pandas as pd
from etl.transform.transform import transform_data


def test_transform_data():
    base_path = os.path.dirname(__file__)
    test_customers_path = os.path.join(
        base_path,
        '../test_data/expected_customers_clean_results.csv'
    )
    test_transactions_path = os.path.join(
        base_path,
        '../test_data/expected_transactions_clean_results.csv'
    )

    expected_merged_data_path = os.path.join(
        base_path,
        '../test_data/expected_merged_clean_results.csv'
    )
    # Create test data for transactions
    transactions_data = pd.read_csv(test_transactions_path)

    # Create test data for customers
    customers_data = pd.read_csv(test_customers_path)

    # Expected merged DataFrame
    expected_merged_data = pd.read_csv(expected_merged_data_path)
    expected_merged_data = expected_merged_data.sort_values(
        by='transaction_id'
    ).reset_index(drop=True)

    expected_merged_data.to_csv(
        'expected_merged_clean_results.csv',
        index=False
    )

    # Call the transform_data function with the test data
    merge_result = transform_data((transactions_data, customers_data))[0]

    merge_result = merge_result.sort_values(by='transaction_id').reset_index(
        drop=True
    )

    # Assert that the result matches the expected DataFrame
    pd.testing.assert_frame_equal(
        merge_result,
        expected_merged_data
    )
