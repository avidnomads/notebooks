"""
Tests for multiplication_methods notebook
"""

import pytest
import sys
# sys.path.insert(0, '../multiplication_methods')
from ..customnumbers import *


@pytest.mark.parametrize("a,b,product", [
    ('0','0','0'), ('0','9','0'),
    ('1','0','0'), ('1','9','9'),
    ('7','3','21'), ('8','5','40'), ('2','9','18'),
])
def test_rational_mult_table(a, b, product):
    assert str(int(a)*int(b)) == product
