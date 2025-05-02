import sqlalchemy
import pytest
from utils.db_utils import get_db_connection, DatabaseConnectionError
from config.db_config import load_db_config


def test_db_connection_success():
    connection_params = load_db_config()["source_database"]
    connection = get_db_connection(connection_params)

    assert isinstance(connection, sqlalchemy.engine.base.Connection)

    # Clean up by closing the connection
    connection.close()


def test_db_connection_unavailable():
    connection_params = load_db_config()["source_database"]
    connection_params["host"] = "unreachable_host"

    with pytest.raises(DatabaseConnectionError):
        get_db_connection(connection_params)


def test_db_connection_already_closed():
    connection_params = load_db_config()["source_database"]
    connection = get_db_connection(connection_params)
    connection.close()

    assert connection.closed
    with pytest.raises(sqlalchemy.exc.ObjectNotExecutableError):
        # Try to execute a query on a closed connection
        connection.execute("SELECT 1")
