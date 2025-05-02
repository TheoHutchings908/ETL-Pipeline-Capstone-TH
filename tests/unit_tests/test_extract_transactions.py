import pytest
import pandas as pd
from etl.extract.extract_transactions import (
    extract_transactions,
    TYPE,
    # EXTRACT_TRANSACTIONS_QUERY_FILE,
    EXPECTED_IMPORT_RATE,
)


@pytest.fixture
def mock_log_extract_success(mocker):
    return mocker.patch("etl.extract.extract_transactions.log_extract_success")


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("etl.extract.extract_transactions.logger")


def test_log_extract_success_transactions(
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
        "etl.extract.extract_transactions.timeit.default_timer",
        side_effect=[mock_start_time, mock_end_time]
    )

    df = extract_transactions()

    # Assertions
    mock_log_extract_success.assert_called_once_with(
        mock_logger,
        TYPE,
        df.shape,
        mock_execution_time,
        EXPECTED_IMPORT_RATE,
    )


def test_log_transactions_error(mocker, mock_logger):
    # Patch the function to raise an exception
    mocker.patch(
        "etl.extract.extract_transactions.extract_transactions_execution",
        side_effect=Exception("Exception message")
    )

    # Test that the exception is raised
    with pytest.raises(Exception, match="Exception message"):
        extract_transactions()

    # Verify that the error was logged
    mock_logger.error.assert_called_once_with(
        "Failed to extract data: Exception message"
    )
