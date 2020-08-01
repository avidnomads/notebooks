"""
Tests for multiplication_methods notebook
"""

import pytest
# import sys
# sys.path.insert(0, '../multiplication_methods')
from ..customnumbers import *


@pytest.mark.parametrize('a,b,product', [
    ('0','0','0'), ('0','9','0'),
    ('1','0','0'), ('1','9','9'),
    ('7','3','21'), ('8','5','40'), ('2','9','18'),
])
def test_Rational_mult_table(a, b, product):
    assert str(int(a)*int(b)) == product

@pytest.mark.parametrize('inputString,expected', [
    ('12345', '12345'),
    ('-12345', '-12345'),
    ('123.45', '123.45'),
    ('-123.45', '-123.45'),
    ('123.450000000000000', '123.45'),
    ('000000000000123.45', '123.45'),
    ('000000000000123.450000000000000', '123.45'),
    ('123000000000000.450000000000000', '123000000000000.45'),
    ('-000000000000123.450000000000000', '-123.45'),
    ('-123000000000000.450000000000000', '-123000000000000.45'),
    ('.1','.1'),
    ('.10','.1'),
    ('-.1','-.1'),
    ('-.10','-.1'),
    ('-0.1','-.1'),
    ('-0.10','-.1'),
    ('0.010','.01'),
    ('-0.010','-.01'),
    ('0.01010','.0101'),
])
def test_Rational_str(inputString, expected):
    r = Rational(inputString)
    assert str(r) == expected 

@pytest.mark.parametrize('digits,highestPower,negative,expected', [
    ([1,2,3], -3, False, '.00123'),
    ([1,2,3], -2, False, '.0123'),
    ([1,2,3], -1, False, '.123'),
    ([1,2,3], 0, False, '1.23'),
    ([1,2,3], 1, False, '12.3'),
    ([1,2,3], 2, False, '123'),
])
def test_Rational_fromDigits(digits,highestPower,negative,expected):
    r = Rational.fromDigits(digits, highestPower, negative)
    assert str(r) == expected 

@pytest.mark.parametrize('digits,highestPower,negative', [
    ([1,2,3], 3, False),
    ([1,2,3], 4, False),
    ([1,2,3], 100, False),
    ([1,2,3], 3, True),
    ([1,2,3], 4, True),
    ([1,2,3], 100, True),
])
def test_Rational_fromDigits_ValueError(digits,highestPower,negative):
    with pytest.raises(ValueError):
        r = Rational.fromDigits(digits, highestPower, negative)
