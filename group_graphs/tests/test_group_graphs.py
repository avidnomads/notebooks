import pytest
from ..group_graphs import *


""" 
    Power tests
"""

@pytest.mark.parametrize('x,n,expected', [
    ('x',0,'x0'),
    ('y',89374,'y89374'),
    ('z',-1,'z-1'),
])
def test_Power_str(x, n, expected):
    assert str(Power(x, n)) == expected

@pytest.mark.parametrize('x,n,expected', [
    ('x', 0, []),
    ('x', 1, [('x', 1)]),
    ('x', 2, [('x', 1), ('x', 1)]),
    ('x', -1, [('x', -1)]),
    ('x', -2, [('x', -1), ('x', -1)]),
    ('x', 1000, [('x', 1)]*1000),
    ('x', -1000, [('x', -1)]*1000),
])
def test_Power_flattened(x, n, expected):
    assert Power(x, n).flattened() == expected

@pytest.mark.parametrize('x1,n1,x2,n2,expected', [
    ('x', 0, 'x', 0, True),
    ('x', 0, 'y', 0, False),
    ('x', 1, 'x', 0, False),
])
def test_Power_eq(x1, n1, x2, n2, expected):
    assert (Power(x1,n1) == Power(x2,n2)) == expected

@pytest.mark.parametrize('x1,n1,x2,n2,expected', [
    ('x', 0, 'x', 0, False),
    ('x', 1, 'x', 0, False),
    ('x', 0, 'x', 1, True),
    ('x', 0, 'y', 0, True),
    ('y', 0, 'x', 0, False),
    ('x', 0, 'y', 1, True),
    ('y', 0, 'x', 1, False),
    ('x', 1, 'y', 0, True),
    ('y', 1, 'x', 0, False),
])
def test_Power_lt(x1, n1, x2, n2, expected):
    assert (Power(x1,n1) < Power(x2,n2)) == expected


""" 
    Word tests
"""

@pytest.mark.parametrize('powers,expected', [
    ([], '1'),
    ([Power('x',0)], 'x0'),
    ([Power('x',1), Power('x',-1)], 'x1x-1'),
    ([Power('x',-1), Power('y',3), Power('z',-2), Power('x',-4), Power('z',1)], 
        'x-1y3z-2x-4z1'),
])
def test_Word_str(powers, expected):
    assert str(Word(powers)) == expected

def test_Word_powersNotShared():
    w1 = Word([Power('x',0)])
    w2 = Word([Power('x',1), Power('x',-1)])
    assert any( [p1 != p2 for p1, p2 in zip(w1.powers, w2.powers)] )

@pytest.mark.parametrize('powers,expected', [
    ([], 0),
    ([Power('x',0)], 0),
    ([Power('x',1), Power('x',-1)], 2),
    ([Power('x',-1), Power('y',3), Power('z',-2), Power('x',-4), Power('z',1)], 
        11),
])
def test_Word_len(powers, expected):
    assert len(Word(powers)) == expected

@pytest.mark.parametrize('powers,expected', [
    ([], []),
    ([Power('x',0)], []),
    ([Power('x',1), Power('x',-1)], [('x',1), ('x',-1)]),
    ([Power('x',-1), Power('y',3), Power('z',-2), Power('x',-4), Power('z',1)], 
        [('x',-1)] + [('y',1)]*3 + [('z',-1)]*2 + [('x',-1)]*4 + [('z',1)]),
])
def test_Word_flattened(powers, expected):
    assert Word(powers).flattened() == expected

@pytest.mark.parametrize('powers1,powers2,expected', [
    ([], [], False),
    ([Power('x',0)], [Power('x',0)], False),
    ([Power('x',1)], [Power('y',1)], True),
    ([Power('x',1)], [Power('x',2)], True),
    ([Power('y',1)], [Power('x',1)], False),
    ([Power('y',1)], [Power('x',2)], True),
    ([Power('x',1), Power('x',1)], [Power('y',1), Power('y',1)], True),
    ([Power('x',-1), Power('y',1)], [Power('y',2)], True),
    ([Power('x',1)], [Power('y',1)], True),
    ([Power('x',1), Power('x',1)], [Power('y',1)], False),
    ([Power('x',1), Power('x',1)], [Power('y',2)], True),
    ([Power('x',1), Power('y',1)], [Power('y',1)], False),
    ([Power('x',1), Power('y',1)], [Power('y',2)], True),
    ([Power('y',1), Power('x',1)], [Power('y',2)], True),
    ([Power('y',1), Power('x',1)], [Power('y',1)], False),
    ([Power('y',-1), Power('x',2), Power('y',1)], 
        [Power('y',-1), Power('x',2), Power('y',-1)], False),
    ([Power('y',-1), Power('x',2), Power('y',1)], 
        [Power('y',-1), Power('x',2)], False),
    ([Power('y',2)], [Power('y',1), Power('x',1)], False),
    ([Power('y',1)], [Power('y',1), Power('x',1)], True),
    ([Power('y',-1), Power('x',2), Power('y',-1)],
        [Power('y',-1), Power('x',2), Power('y',1)], True),
    ([Power('y',-1), Power('x',2)], 
        [Power('y',-1), Power('x',2), Power('y',1)], True),
])
def test_Word_lt(powers1, powers2, expected):
    assert (Word(powers1) < Word(powers2)) == expected

@pytest.mark.parametrize('powers', [
    ([],),
    ([Power('x',0)],),
    ([Power('x',12345)],),
    ([Power('x',-1), Power('y',2), Power('x',1), Power('z',-7), Power('y',2)],),
])
def test_Word_copy(powers):
    w1 = Word(powers)
    w2 = w1.copy()
    assert all( [p1 == p2 for p1, p2 in zip(w1.powers, w2.powers)] )

@pytest.mark.parametrize('word,power,expected', [
    (Word(), Power('x',123), 'x123'),
    (Word(), Power('x',0), '1'),
    (Word([Power('x',3)]), Power('x',0), 'x3'),
    (Word([Power('x',123)]), Power('x',-123), '1'),
    (Word([Power('x',-3)]), Power('x',9), 'x6'),
    (Word([Power('x',-3)]), Power('y',9), 'x-3y9'),
    (Word([Power('x',-3), Power('y',-9)]), Power('y',9), 'x-3'),
])
def test_Word_extend_right(word, power, expected):
    word.extend_right(power)
    assert str(word) == expected

@pytest.mark.parametrize('powerTuples,expected', [
    ([], '1'),
    ([('x',0)], '1'),
    ([('x',1), ('x',-1),], '1'),
    ([('x',12), ('x',-8), ('x',-9), ('x',5),], '1'),
    ([('x',1), ('y',1), ('z',1), ('z',-1), ('y',-1), ('x',-1),], '1'),
    ([('x',-1), ('y',-1), ('x',3), ('x',-1), ('x',-1), ('x',1), ('x',-2), ('y',2), ('y',1), ('y',-2), ('x',1), ('z',30), ('z',-31)], 
        'z-1'),
    ([('x',1), ('x',-1), ('y',1)], 'y1'),
    ([('x',1), ('y',1), ('z',-3), ('z',3), ('y',7)], 'x1y8'),
])
def test_Word_fromList(powerTuples, expected):
    assert str(Word.fromList(powerTuples)) == expected