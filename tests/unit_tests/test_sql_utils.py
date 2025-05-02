import pytest
from utils.db_utils import QueryExecutionError
from utils.sql_utils import import_sql_query


def test_import_sql_query_success_logging(mocker):
    # Setup
    filename = "tests/unit_tests/test_data/test_query.sql"
    expected_query = "SELECT * FROM test_table"
    mocker.patch("builtins.open", mocker.mock_open(read_data=expected_query))
    mock_logger = mocker.patch("utils.sql_utils.logger")

    # Run
    result = import_sql_query(filename)

    # Check
    mock_logger.info.assert_called_once_with(
        f"Successfully imported query from {filename}"
    )
    assert result == expected_query


def test_import_sql_query_failure_logging(mocker):
    # Setup
    filename = "tests/unit_tests/test_data/missing_query.sql"
    error_message = f"Failed to import query: {filename} not found"
    mocker.patch(
        "builtins.open",
        side_effect=FileNotFoundError(error_message)
    )
    mock_logger = mocker.patch("utils.sql_utils.logger")

    # Run and check
    with pytest.raises(QueryExecutionError):
        import_sql_query(filename)

    mock_logger.error.assert_called_once_with(error_message)
