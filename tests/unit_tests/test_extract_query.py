import pytest
import pandas as pd
from unittest.mock import MagicMock, call
from etl.extract.extract_query import execute_extract_query
from utils.db_utils import QueryExecutionError


def test_function_calls_pandas_read_sql_query(mocker):
    # Arrange
    mock_read_sql_query = mocker.patch("pandas.read_sql_query")
    mock_connection = MagicMock()
    query = "SELECT * FROM transactions"

    # Act
    execute_extract_query(query, mock_connection)

    # Assert
    mock_read_sql_query.assert_called_once_with(query, mock_connection)


def test_execute_extract_query_invalid_query(mocker):
    mock_read_sql = mocker.patch(
        "pandas.read_sql_query",
        side_effect=pd.errors.DatabaseError("Invalid query"),
    )
    mock_connection = MagicMock()
    query = "SELECT unrecognized_column FROM transactions"

    with pytest.raises(QueryExecutionError):
        execute_extract_query(query, mock_connection)

    mock_read_sql.assert_called_once_with(query, mock_connection)


def test_execute_extract_query_invalid_query_logging(mocker):
    # Mock the logger
    mock_logger = mocker.patch("etl.extract.extract_query.logger")

    # Mock the pandas read_sql_query function to raise a DatabaseError
    mocker.patch(
        "pandas.read_sql_query",
        side_effect=pd.errors.DatabaseError("Invalid query"),
    )
    mock_connection = MagicMock()
    query = "SELECT unrecognized_column FROM transactions"

    with pytest.raises(QueryExecutionError):
        execute_extract_query(query, mock_connection)

    mock_logger.error.assert_has_calls(
        [
            call("Failed to execute query: Invalid query"),
            call(f"The query that failed was: {query}"),
        ]
    )
