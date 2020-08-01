import pytest
from ..group_graphs import *


@pytest.mark.parametrize('x,n,expected', [
    ('x','0','x0'),
    ('y','89374','y89374'),
    ('z','-1','z-1'),
])
def test_Power_str(x, n, expected):
    assert str(Power(x, n)) == expected
