import pytest
from ..customnumbers import *


@pytest.mark.parametrize('inputString,expected', [
    ('0', '0'),
    ('171712345', '171712345'),
    ('000', '0'),
    ('000001', '1'),
    ('00000100', '100'),
])
def test_Number_str(inputString, expected):
    assert str(Number(inputString)) == expected