import pytest
import logging
from dnacommon.ep_logging import name_as_level


@pytest.mark.parametrize("test_input, expected", [
    ("deBug", logging.DEBUG),
    ("debug", logging.DEBUG),
    ("ERROR", logging.ERROR),
    ("Deb", logging.INFO),
    (None, logging.INFO)
])
def test_name_as_level(test_input, expected):
    assert name_as_level(test_input) is expected
