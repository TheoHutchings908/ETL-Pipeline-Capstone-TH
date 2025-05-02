import timeit
from etl.extract.extract_customers import (
    extract_customers,
    EXPECTED_PERFORMANCE
)


def test_extract_customers_returns_all_data():
    expected_shape = (5200, 5)
    # Call the function to get the DataFrame
    df = extract_customers()

    # Verify the dimensions of the DataFrame
    assert df.shape == expected_shape, (
        f"Expected DataFrame shape to be {expected_shape}, but got {df.shape}"
    )


def test_extract_customers_performance():
    execution_time = timeit.timeit(
        "extract_customers()",
        globals=globals(),
        number=1
    )

    # Call the function to get the DataFrame
    df = extract_customers()

    # Load time per row
    actual_execution_time_per_row = execution_time / df.shape[0]

    # Assert that the execution time is within an acceptable range
    assert actual_execution_time_per_row <= EXPECTED_PERFORMANCE, (
        f"Expected execution time to be less than or equal to "
        f"{str(EXPECTED_PERFORMANCE)} seconds, but got "
        f"{str(actual_execution_time_per_row)} seconds"
    )
