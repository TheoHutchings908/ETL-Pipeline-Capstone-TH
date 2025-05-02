import pytest

from sqlalchemy.exc import SQLAlchemyError, OperationalError
from unittest.mock import MagicMock
from utils.db_utils import (
    get_db_connection,
    create_db_engine,
    DatabaseConnectionError,
)


@pytest.fixture
def connection_params():
    return {
        "dbname": "test_db",
        "user": "test_user",
        "password": "test_password",
        "host": "test_host",
        "port": "1234",
    }


def test_get_db_connection_success(mocker, connection_params):
    # Arrange
    mock_connection = MagicMock()
    mock_engine = MagicMock()
    mock_engine.connect.return_value = mock_connection

    mock_get_engine = mocker.patch(
        "utils.db_utils.create_db_engine", return_value=mock_engine
    )

    # Act
    connection = get_db_connection(connection_params)

    # Assert
    mock_get_engine.assert_called_once_with(connection_params)
    mock_engine.connect.assert_called_once()
    assert connection == mock_connection


def test_get_db_connection_success_logging(mocker, connection_params):
    mock_logger = mocker.patch("utils.db_utils.logger")
    mock_connection = MagicMock()
    mock_engine = MagicMock()
    mock_engine.connect.return_value = mock_connection

    mocker.patch("utils.db_utils.create_db_engine", return_value=mock_engine)

    get_db_connection(connection_params)

    mock_logger.info.assert_called_once_with(
        "Successfully connected to the database."
    )


def test_get_db_connection_failure(mocker, connection_params):
    mock_connect = mocker.patch(
        "utils.db_utils.create_engine",
        side_effect=SQLAlchemyError("Connection error"),
    )
    mock_logger = mocker.patch("utils.db_utils.logger")

    expected_connection_string = (
        f"postgresql+psycopg2://{connection_params['user']}:"
        f"{connection_params['password']}@{connection_params['host']}:"
        f"{int(connection_params['port'])}/{connection_params['dbname']}"
    )

    with pytest.raises(DatabaseConnectionError) as excinfo:
        get_db_connection(connection_params)

    assert str(excinfo.value) == (
        "Failed to connect to the database: Connection error"
    )
    mock_connect.assert_called_once_with(expected_connection_string)
    mock_logger.error.assert_called_once_with(
        "Failed to connect to the database: Connection error"
    )


def test_get_db_connection_timeout_failure(mocker, connection_params):
    mocker.patch(
        "utils.db_utils.create_engine",
        side_effect=OperationalError("timeout", None, None),
    )
    mock_logger = mocker.patch("utils.db_utils.logger")

    with pytest.raises(DatabaseConnectionError) as excinfo:
        get_db_connection(connection_params)

    print(str(excinfo.value))
    assert "timeout" in str(excinfo.value)

    mock_logger.error.assert_called_once_with(str(excinfo.value))


# Define a set of connection parameters that are invalid
# These should be used as parameterised inputs for the test
# The function should through a ValueError if connection parameters are invalid
@pytest.mark.parametrize(
    "invalid_params",
    [
        {
            "dbname": "",
            "user": "test_user",
            "password": "test_password",
            "host": "test_host",
            "port": "1234",
        },
        {
            "dbname": "test_db",
            "user": "",
            "password": "test_password",
            "host": "test_host",
            "port": "1234",
        },
        {
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_password",
            "host": "",
            "port": "1234",
        },
        {
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_password",
            "host": "test_host",
            "port": "",
        },
        {
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_password",
            "host": "test_host",
            "port": "NaN",
        },
    ],
)
def test_create_db_engine_invalid_params(mocker, invalid_params):
    mock_logger = mocker.patch("utils.db_utils.logger")

    with pytest.raises(DatabaseConnectionError) as excinfo:
        create_db_engine(invalid_params)

    assert "Invalid Connection Parameters" in str(excinfo.value)
    mock_logger.error.assert_called_once_with(str(excinfo.value))


def test_create_db_engine_success(mocker, connection_params):
    mock_engine = MagicMock()
    mock_create_engine = mocker.patch(
        "utils.db_utils.create_engine", return_value=mock_engine
    )

    engine = create_db_engine(connection_params)

    expected_connection_string = (
        f"postgresql+psycopg2://{connection_params['user']}:"
        f"{connection_params['password']}@{connection_params['host']}:"
        f"{int(connection_params['port'])}/{connection_params['dbname']}"
    )

    mock_create_engine.assert_called_once_with(expected_connection_string)
    assert engine == mock_engine


def test_create_db_engine_success_logging(mocker, connection_params):
    mock_logger = mocker.patch("utils.db_utils.logger")
    mock_engine = MagicMock()
    mocker.patch("utils.db_utils.create_engine", return_value=mock_engine)

    create_db_engine(connection_params)

    mock_logger.info.assert_called_once_with(
        "Successfully created the database engine."
    )


def test_create_db_engine_failure(mocker, connection_params):
    mock_create_engine = mocker.patch(
        "utils.db_utils.create_engine",
        side_effect=ValueError("Invalid connection parameters"),
    )
    mock_logger = mocker.patch("utils.db_utils.logger")

    with pytest.raises(DatabaseConnectionError) as excinfo:
        create_db_engine(connection_params)

    assert "Invalid Connection Parameters" in str(excinfo.value)
    mock_create_engine.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Invalid Connection Parameters: Invalid connection parameters"
    )
