import pytest
from etl.transform.clean_customers import standardise_is_active


# Create a list of pytest parameters for the different values of is_active
@pytest.mark.parametrize(
    'is_active_value, expected',
    [
        ('active', True),
        ('1', True),
        ('True', True),
        (True, True),
        ('inactive', False),
        ('0', False),
        ('False', False),
        (False, False),
        (None, False),
    ]
)
def test_standardise_is_active(is_active_value, expected):
    assert standardise_is_active(is_active_value) == expected
