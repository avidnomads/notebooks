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

@pytest.mark.parametrize("inputString,stringRep", [
    ("12345", "12345"),
    ("-12345", "-12345"),
    ("123.45", "123.45"),
    ("-123.45", "-123.45"),
    ("123.450000000000000", "123.45"),
    ("000000000000123.45", "123.45"),
    ("000000000000123.450000000000000", "123.45"),
    ("123000000000000.450000000000000", "123000000000000.45"),
    ("-000000000000123.450000000000000", "-123.45"),
    ("-123000000000000.450000000000000", "-123000000000000.45"),
])
def test_init_stringRep(inputString, stringRep):
    r = Rational(inputString)
    assert(r.stringRep == stringRep)
