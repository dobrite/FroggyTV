import pytest
from helpers.utils import TestOutput


@pytest.fixture
def test_output():
    return TestOutput()
