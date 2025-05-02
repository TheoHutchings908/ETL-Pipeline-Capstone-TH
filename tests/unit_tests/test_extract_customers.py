import pytest
import pandas as pd
from etl.extract.extract_customers import (
    extract_customers,
    TYPE,
    FILE_PATH,
    EXPECTED_PERFORMANCE,
)


@pytest.fixture
def mock_log_extract_success(mocker):
    return mocker.patch("etl.extract.extract_customers.log_extract_success")


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("etl.extract.extract_customers.logger")


def test_log_extract_success_customers(
    mocker,
    mock_log_extract_success,
    mock_logger
):
    mock_execution_time = 0.5
    mock_df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie']
    })
    mocker.patch(
        "etl.extract.extract_customers.pd.read_csv",
        return_value=mock_df
    )

    # Mock timeit.default_timer to control the execution time
    mock_start_time = 100.0
    mock_end_time = 100.5
    mocker.patch(
        "etl.extract.extract_customers.timeit.default_timer",
        side_effect=[mock_start_time, mock_end_time]
    )

    # Call the function
    df = extract_customers()

    # Assertions
    mock_log_extract_success.assert_called_once_with(
        mock_logger,
        TYPE,
        df.shape,
        mock_execution_time,
        EXPECTED_PERFORMANCE
    )


def test_log_customers_error(mocker, mock_logger):
    # Mock pd.read_csv to raise an exception
    mocker.patch(
        "etl.extract.extract_customers.pd.read_csv",
        side_effect=Exception(
            f"Failed to load CSV file: {FILE_PATH}"
        )
    )

    # Call the function and assert exception
    with pytest.raises(
        Exception,
        match=f"Failed to load CSV file: {FILE_PATH}"
    ):
        extract_customers()

    # Verify that the error was logged
    mock_logger.error.assert_called_once_with(
         f"Error loading {FILE_PATH}: Failed to load CSV file: {FILE_PATH}"
    )
