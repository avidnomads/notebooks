import pytest


@pytest.mark.parametrize('a,b', [
    (0, 0),
])
def test_default(a, b):
    assert a == b